"""
Parser de XMLs de NF-e (modelo 55) e NFCom (modelo 62).
Extrai dados da nota e itens, incluindo IBS/CBS quando presentes.
"""

import logging
from pathlib import Path
from decimal import Decimal
from datetime import datetime
from typing import Optional
from lxml import etree

from .models import NFe, Item, Tributos, IBSCBSData
from .config import Config, XPathConfig
from .utils import (
    extract_text_safe,
    extract_decimal_safe,
    find_with_xpaths,
    to_decimal,
)

logger = logging.getLogger(__name__)


class NFeParser:
    """Parser de XML de NF-e (modelo 55) e NFCom (modelo 62) com suporte a IBS/CBS."""
    
    def __init__(self, config: Config):
        """
        Inicializa parser.
        
        Args:
            config: Configuração do sistema
        """
        self.config = config
    
    def parse_file(self, xml_path: Path) -> Optional[NFe]:
        """
        Faz parse de um arquivo XML de NF-e ou NFCom.
        
        Args:
            xml_path: Caminho do arquivo XML
        
        Returns:
            Objeto NFe ou None em caso de erro
        """
        try:
            tree = etree.parse(str(xml_path))
            root = tree.getroot()
            
            # Detectar e tratar vários tipos de documento
            # 1) infNFe / infNFCom (nota fiscal)
            inf_doc = self._find_inf_document(root)
            if inf_doc is not None:
                # Extrair dados como NF-e/NFCom
                nfe = self._extract_nfe_data(inf_doc, xml_path.name)
                self._extract_items(inf_doc, nfe)
                try:
                    nfe.tags = self._collect_all_tags(inf_doc)
                except Exception:
                    nfe.tags = {}

                logger.debug(f"Parsed {xml_path.name}: {len(nfe.itens)} itens")
                return nfe

            # 2) retNFCom / protNFCom (protocolo de autorização) - extrair infProt
            prot = root.xpath(".//*[local-name()='infProt']")
            if prot:
                node = prot[0]
                nfe = NFe(chave=extract_text_safe(node, ".//*[local-name()='chNFCom']"), arquivo=xml_path.name)
                try:
                    nfe.tags = self._collect_all_tags(node)
                except Exception:
                    nfe.tags = {}
                logger.debug(f"Parsed protocolo {xml_path.name}: chave {nfe.chave}")
                return nfe

            # 3) UBL / Sovos canonical invoice -> buscar inv:Invoice ou elemento local-name() = 'Invoice'
            inv = root.xpath(".//*[local-name()='Invoice']")
            if inv:
                node = inv[0]
                # tentar obter UUID/cbc:UUID ou ID
                chave = extract_text_safe(node, ".//*[local-name()='UUID']") or extract_text_safe(node, ".//*[local-name()='ID']")
                nfe = NFe(chave=chave or '', arquivo=xml_path.name)
                try:
                    nfe.tags = self._collect_all_tags(node)
                except Exception:
                    nfe.tags = {}
                logger.debug(f"Parsed UBL Invoice {xml_path.name}: chave {nfe.chave}")
                return nfe

            # 4) DPS / NFS-e (infDPS)
            inf_dps = root.xpath(".//*[local-name()='infDPS']")
            if inf_dps:
                node = inf_dps[0]
                chave = node.get('Id', '')
                # nDPS as fallback
                if not chave:
                    chave = extract_text_safe(node, ".//*[local-name()='nDPS']")
                nfe = NFe(chave=chave or '', arquivo=xml_path.name)
                try:
                    nfe.tags = self._collect_all_tags(node)
                except Exception:
                    nfe.tags = {}
                logger.debug(f"Parsed DPS {xml_path.name}: chave {nfe.chave}")
                return nfe

            # 5) TXT key=value (fallback for non-XML structured txt files)
            # Note: this branch is reached only for parsed XML-like inputs; TXT files are handled elsewhere by CLI file listing.
            logger.error(f"Elemento infNFe/infNFCom/infDPS/Invoice/protNFCom não encontrado em {xml_path.name}")
            return None
            
            logger.debug(f"Parsed {xml_path.name}: {len(nfe.itens)} itens")
            return nfe
            
        except etree.XMLSyntaxError as e:
            # Tentar interpretar como arquivo TXT chave=valor (se aplicável)
            try:
                text = Path(xml_path).read_text(encoding='utf-8', errors='ignore')
                parts = text.split('|')
                tags = {}
                chave = ''
                for p in parts:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        k = k.strip()
                        v = v.strip()
                        tags[f'TXT/{k}'] = v
                        if k.lower() in ('numerorps', 'ndps', 'ndps', 'numerorps') and not chave:
                            chave = v
                if not chave:
                    # tentar extrair algum identificador genérico
                    chave = tags.get('TXT/numeroRps', '') or tags.get('TXT/nDPS', '')
                nfe = NFe(chave=chave or '', arquivo=xml_path.name)
                nfe.tags = tags
                logger.debug(f"Parsed TXT fallback {xml_path.name}: keys {len(tags)}")
                return nfe
            except Exception:
                logger.error(f"Erro de sintaxe XML em {xml_path.name}: {e}")
                return None
        except Exception as e:
            logger.error(f"Erro ao processar {xml_path.name}: {e}", exc_info=True)
            return None
    
    def _find_inf_document(self, root: etree._Element) -> Optional[etree._Element]:
        """
        Encontra elemento infNFe ou infNFCom independente de namespace.
        
        Args:
            root: Elemento raiz do XML
        
        Returns:
            Elemento infNFe/infNFCom ou None
        """
        # Tentar com local-name (ignora namespace)
        xpaths = [
            ".//*[local-name()='infNFe']",
            ".//*[local-name()='infNFCom']",
            ".//infNFe",
            ".//infNFCom",
        ]
        
        for xpath in xpaths:
            try:
                result = root.xpath(xpath)
                if result:
                    return result[0]
            except Exception:
                continue
        
        return None
    
    def _extract_nfe_data(self, inf_nfe: etree._Element, arquivo: str) -> NFe:
        """
        Extrai dados principais da NF-e ou NFCom.
        
        Args:
            inf_nfe: Elemento infNFe ou infNFCom
            arquivo: Nome do arquivo
        
        Returns:
            Objeto NFe
        """
        # Chave de acesso (atributo Id)
        chave = inf_nfe.get("Id", "")
        if chave.startswith("NFe"):
            chave = chave[3:]
        elif chave.startswith("NFCom"):
            chave = chave[5:]
        
        # Identificação
        ide = inf_nfe.xpath(".//*[local-name()='ide']")[0]
        nNF = extract_text_safe(ide, ".//*[local-name()='nNF']")
        serie = extract_text_safe(ide, ".//*[local-name()='serie']", "0")
        
        # Data de emissão
        dh_emi_str = extract_text_safe(ide, ".//*[local-name()='dhEmi']")
        try:
            dhEmi = datetime.fromisoformat(dh_emi_str.replace("Z", "+00:00"))
        except Exception:
            dhEmi = datetime.now()
        
        # Emitente
        emit = inf_nfe.xpath(".//*[local-name()='emit']")[0]
        emit_CNPJ = extract_text_safe(emit, ".//*[local-name()='CNPJ']")
        emit_xNome = extract_text_safe(emit, ".//*[local-name()='xNome']")
        emit_UF = extract_text_safe(emit, ".//*[local-name()='enderEmit']/*[local-name()='UF']")
        
        # Destinatário
        dest_elements = inf_nfe.xpath(".//*[local-name()='dest']")
        dest_CNPJ = ""
        dest_CPF = ""
        dest_xNome = ""
        dest_UF = ""
        
        if dest_elements:
            dest = dest_elements[0]
            dest_CNPJ = extract_text_safe(dest, ".//*[local-name()='CNPJ']")
            dest_CPF = extract_text_safe(dest, ".//*[local-name()='CPF']")
            dest_xNome = extract_text_safe(dest, ".//*[local-name()='xNome']")
            dest_UF = extract_text_safe(dest, ".//*[local-name()='enderDest']/*[local-name()='UF']")
        
        # Totais
        total = inf_nfe.xpath(".//*[local-name()='total']/*[local-name()='ICMSTot']")[0]
        vNF = extract_decimal_safe(total, ".//*[local-name()='vNF']")
        vProd_total = extract_decimal_safe(total, ".//*[local-name()='vProd']")
        
        return NFe(
            chave=chave,
            nNF=nNF,
            serie=serie,
            dhEmi=dhEmi,
            emit_CNPJ=emit_CNPJ,
            emit_xNome=emit_xNome,
            emit_UF=emit_UF,
            dest_CNPJ=dest_CNPJ,
            dest_CPF=dest_CPF,
            dest_xNome=dest_xNome,
            dest_UF=dest_UF,
            vNF=vNF,
            vProd_total=vProd_total,
            arquivo=arquivo,
        )
    
    def _extract_items(self, inf_nfe: etree._Element, nfe: NFe):
        """
        Extrai itens da NF-e ou NFCom.
        
        Args:
            inf_nfe: Elemento infNFe ou infNFCom
            nfe: Objeto NFe para adicionar itens
        """
        det_list = inf_nfe.xpath(".//*[local-name()='det']")
        
        for det in det_list:
            try:
                item = self._extract_item(det)
                if item:
                    nfe.itens.append(item)
            except Exception as e:
                nItem = det.get("nItem", "?")
                logger.warning(f"Erro ao extrair item {nItem} de {nfe.arquivo}: {e}")

    def _collect_all_tags(self, inf_nfe: etree._Element) -> dict:
        """
        Percorre todos os elementos abaixo de infNFe/infNFCom e retorna um dicionário
        com o caminho composto por nomes locais e o texto (ou string vazia).
        """
        tags = {}

        def local_name(elem):
            return etree.QName(elem).localname

        # Detectar tipo de documento (infNFe ou infNFCom)
        root_name = local_name(inf_nfe)

        for elem in inf_nfe.xpath('.//*'):
            try:
                parts = []
                node = elem
                # subir até inf_nfe/inf_nfcom
                while node is not None and node != inf_nfe:
                    parts.insert(0, local_name(node))
                    node = node.getparent()

                # prefix with infNFe or infNFCom
                path = f'{root_name}/' + '/'.join(parts) if parts else root_name
                text = elem.text.strip() if (elem.text and elem.text.strip() != '') else ''
                tags[path] = text
            except Exception:
                continue

        return tags
    
    def _extract_item(self, det: etree._Element) -> Optional[Item]:
        """
        Extrai dados de um item.
        
        Args:
            det: Elemento det
        
        Returns:
            Objeto Item ou None
        """
        nItem = int(det.get("nItem", "0"))
        
        # Produto
        prod = det.xpath(".//*[local-name()='prod']")[0]
        
        cProd = extract_text_safe(prod, ".//*[local-name()='cProd']")
        xProd = extract_text_safe(prod, ".//*[local-name()='xProd']")
        NCM = extract_text_safe(prod, ".//*[local-name()='NCM']")
        CFOP = extract_text_safe(prod, ".//*[local-name()='CFOP']")
        uCom = extract_text_safe(prod, ".//*[local-name()='uCom']")
        qCom = extract_decimal_safe(prod, ".//*[local-name()='qCom']")
        vUnCom = extract_decimal_safe(prod, ".//*[local-name()='vUnCom']")
        vProd = extract_decimal_safe(prod, ".//*[local-name()='vProd']")
        
        # Componentes opcionais do produto
        vFrete = extract_decimal_safe(prod, ".//*[local-name()='vFrete']")
        vSeg = extract_decimal_safe(prod, ".//*[local-name()='vSeg']")
        vOutro = extract_decimal_safe(prod, ".//*[local-name()='vOutro']")
        vDesc = extract_decimal_safe(prod, ".//*[local-name()='vDesc']")
        
        # Tributos
        tributos = self._extract_tributos(det)
        
        # IBS/CBS do XML
        ibs_xml = self._extract_ibs_cbs(det, self.config.xpaths.ibs)
        cbs_xml = self._extract_ibs_cbs(det, self.config.xpaths.cbs)
        
        return Item(
            nItem=nItem,
            cProd=cProd,
            xProd=xProd,
            NCM=NCM,
            CFOP=CFOP,
            uCom=uCom,
            qCom=qCom,
            vUnCom=vUnCom,
            vProd=vProd,
            vFrete=vFrete,
            vSeg=vSeg,
            vOutro=vOutro,
            vDesc=vDesc,
            tributos=tributos,
            ibs_xml=ibs_xml,
            cbs_xml=cbs_xml,
        )
    
    def _extract_tributos(self, det: etree._Element) -> Tributos:
        """
        Extrai tributos opcionais do item.
        
        Args:
            det: Elemento det
        
        Returns:
            Objeto Tributos
        """
        imposto = det.xpath(".//*[local-name()='imposto']")
        if not imposto:
            return Tributos()
        
        imposto = imposto[0]
        
        # IPI
        vIPI = Decimal("0")
        ipi_elements = imposto.xpath(".//*[local-name()='IPI']")
        if ipi_elements:
            vIPI = extract_decimal_safe(ipi_elements[0], ".//*[local-name()='vIPI']")
        
        # II
        vII = Decimal("0")
        ii_elements = imposto.xpath(".//*[local-name()='II']")
        if ii_elements:
            vII = extract_decimal_safe(ii_elements[0], ".//*[local-name()='vII']")
        
        # ICMS ST
        vICMSST = Decimal("0")
        icms_elements = imposto.xpath(".//*[local-name()='ICMS']")
        if icms_elements:
            # Pode estar em várias tags: vICMSST, vICMSSTRet, etc.
            vICMSST = extract_decimal_safe(icms_elements[0], ".//*[local-name()='vICMSST']")
            if vICMSST == Decimal("0"):
                vICMSST = extract_decimal_safe(icms_elements[0], ".//*[local-name()='vICMSSTRet']")
        
        # FCP ST
        vFCPST = Decimal("0")
        if icms_elements:
            vFCPST = extract_decimal_safe(icms_elements[0], ".//*[local-name()='vFCPST']")
            if vFCPST == Decimal("0"):
                vFCPST = extract_decimal_safe(icms_elements[0], ".//*[local-name()='vFCPSTRet']")
        
        # PIS
        vPIS = Decimal("0")
        pis_elements = imposto.xpath(".//*[local-name()='PIS']")
        if pis_elements:
            vPIS = extract_decimal_safe(pis_elements[0], ".//*[local-name()='vPIS']")
        
        # COFINS
        vCOFINS = Decimal("0")
        cofins_elements = imposto.xpath(".//*[local-name()='COFINS']")
        if cofins_elements:
            vCOFINS = extract_decimal_safe(cofins_elements[0], ".//*[local-name()='vCOFINS']")
        
        return Tributos(
            vIPI=vIPI,
            vII=vII,
            vICMSST=vICMSST,
            vFCPST=vFCPST,
            vPIS=vPIS,
            vCOFINS=vCOFINS,
        )
    
    def _extract_ibs_cbs(self, det: etree._Element, xpath_config: XPathConfig) -> IBSCBSData:
        """
        Extrai dados de IBS ou CBS usando XPaths configuráveis.
        
        Args:
            det: Elemento det (item)
            xpath_config: Configuração de XPaths para busca
        
        Returns:
            Objeto IBSCBSData
        """
        data = IBSCBSData()
        
        # Buscar base de cálculo
        vbc_str = find_with_xpaths(det, xpath_config.base_paths)
        if vbc_str:
            data.vBC = to_decimal(vbc_str)
            data.found = True
        
        # Buscar alíquota
        aliq_str = find_with_xpaths(det, xpath_config.rate_paths)
        if aliq_str:
            data.pAliq = to_decimal(aliq_str)
            data.found = True
        
        # Buscar valor do tributo
        vtrib_str = find_with_xpaths(det, xpath_config.value_paths)
        if vtrib_str:
            data.vTributo = to_decimal(vtrib_str)
            data.found = True
        
        return data
