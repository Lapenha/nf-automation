"""
Modelos de dados para NF-e, itens e resultados de comparação.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ValidationStatus(Enum):
    """Status de validação de um item ou NF-e."""
    OK = "OK"
    DIVERGENTE = "DIVERGENTE"
    SEM_TAG = "SEM_TAG"
    ERRO = "ERRO"


@dataclass
class Tributos:
    """Dados de tributos de um item (opcionais)."""
    vIPI: Decimal = Decimal("0")
    vII: Decimal = Decimal("0")
    vICMSST: Decimal = Decimal("0")
    vFCPST: Decimal = Decimal("0")
    vPIS: Decimal = Decimal("0")
    vCOFINS: Decimal = Decimal("0")


@dataclass
class IBSCBSData:
    """Dados de IBS ou CBS extraídos do XML."""
    vBC: Optional[Decimal] = None  # Base de cálculo informada
    pAliq: Optional[Decimal] = None  # Alíquota informada
    vTributo: Optional[Decimal] = None  # Valor do tributo informado
    found: bool = False  # Se foi encontrado no XML


@dataclass
class Item:
    """Representa um item (det) da NF-e."""
    nItem: int
    cProd: str
    xProd: str
    NCM: str
    CFOP: str
    uCom: str
    qCom: Decimal
    vUnCom: Decimal
    vProd: Decimal
    vFrete: Decimal = Decimal("0")
    vSeg: Decimal = Decimal("0")
    vOutro: Decimal = Decimal("0")
    vDesc: Decimal = Decimal("0")
    tributos: Tributos = field(default_factory=Tributos)
    
    # Dados IBS/CBS extraídos do XML
    ibs_xml: IBSCBSData = field(default_factory=IBSCBSData)
    cbs_xml: IBSCBSData = field(default_factory=IBSCBSData)
    
    # Bases calculadas (preenchidas pelo calculator)
    base_calculada_ibs: Optional[Decimal] = None
    base_calculada_cbs: Optional[Decimal] = None


@dataclass
class NFe:
    """Representa uma NF-e completa."""
    chave: str
    nNF: str
    serie: str
    dhEmi: datetime
    
    # Emitente
    emit_CNPJ: str
    emit_xNome: str
    emit_UF: str
    
    # Destinatário
    dest_CNPJ: str = ""
    dest_CPF: str = ""
    dest_xNome: str = ""
    dest_UF: str = ""
    
    # Totais da NF
    vNF: Decimal = Decimal("0")
    vProd_total: Decimal = Decimal("0")
    
    # Itens
    itens: List[Item] = field(default_factory=list)
    
    # Metadados
    arquivo: str = ""
    error_message: Optional[str] = None


@dataclass
class ItemComparisonResult:
    """Resultado da comparação de um item específico."""
    nItem: int
    cProd: str
    xProd: str
    
    # Valores calculados
    base_calc_ibs: Decimal
    base_calc_cbs: Decimal
    
    # Valores XML IBS
    base_xml_ibs: Optional[Decimal]
    aliq_xml_ibs: Optional[Decimal]
    valor_xml_ibs: Optional[Decimal]
    
    # Valores XML CBS
    base_xml_cbs: Optional[Decimal]
    aliq_xml_cbs: Optional[Decimal]
    valor_xml_cbs: Optional[Decimal]
    
    # Deltas IBS
    delta_base_ibs: Optional[Decimal] = None
    delta_valor_ibs: Optional[Decimal] = None
    
    # Deltas CBS
    delta_base_cbs: Optional[Decimal] = None
    delta_valor_cbs: Optional[Decimal] = None
    
    # Status
    status_ibs: ValidationStatus = ValidationStatus.SEM_TAG
    status_cbs: ValidationStatus = ValidationStatus.SEM_TAG
    status_geral: ValidationStatus = ValidationStatus.OK
    
    # Flags de divergência
    diverge_base_ibs: bool = False
    diverge_valor_ibs: bool = False
    diverge_base_cbs: bool = False
    diverge_valor_cbs: bool = False


@dataclass
class ComparisonResult:
    """Resultado da comparação de uma NF-e completa."""
    nfe: NFe
    itens_resultado: List[ItemComparisonResult] = field(default_factory=list)
    
    # Totalizadores
    total_itens: int = 0
    total_base_calc_ibs: Decimal = Decimal("0")
    total_base_calc_cbs: Decimal = Decimal("0")
    total_base_xml_ibs: Decimal = Decimal("0")
    total_base_xml_cbs: Decimal = Decimal("0")
    total_valor_xml_ibs: Decimal = Decimal("0")
    total_valor_xml_cbs: Decimal = Decimal("0")
    
    # Contadores
    count_divergencias_ibs: int = 0
    count_divergencias_cbs: int = 0
    count_sem_tag_ibs: int = 0
    count_sem_tag_cbs: int = 0
    
    # Status geral da NF
    status_geral: ValidationStatus = ValidationStatus.OK
    
    def calcular_totais(self):
        """Calcula totais e contadores baseado nos itens."""
        self.total_itens = len(self.itens_resultado)
        
        self.total_base_calc_ibs = sum(
            (item.base_calc_ibs for item in self.itens_resultado),
            Decimal("0")
        )
        self.total_base_calc_cbs = sum(
            (item.base_calc_cbs for item in self.itens_resultado),
            Decimal("0")
        )
        
        self.total_base_xml_ibs = sum(
            (item.base_xml_ibs for item in self.itens_resultado if item.base_xml_ibs),
            Decimal("0")
        )
        self.total_base_xml_cbs = sum(
            (item.base_xml_cbs for item in self.itens_resultado if item.base_xml_cbs),
            Decimal("0")
        )
        
        self.total_valor_xml_ibs = sum(
            (item.valor_xml_ibs for item in self.itens_resultado if item.valor_xml_ibs),
            Decimal("0")
        )
        self.total_valor_xml_cbs = sum(
            (item.valor_xml_cbs for item in self.itens_resultado if item.valor_xml_cbs),
            Decimal("0")
        )
        
        # Contar divergências
        for item in self.itens_resultado:
            if item.status_ibs == ValidationStatus.DIVERGENTE:
                self.count_divergencias_ibs += 1
            elif item.status_ibs == ValidationStatus.SEM_TAG:
                self.count_sem_tag_ibs += 1
            
            if item.status_cbs == ValidationStatus.DIVERGENTE:
                self.count_divergencias_cbs += 1
            elif item.status_cbs == ValidationStatus.SEM_TAG:
                self.count_sem_tag_cbs += 1
        
        # Determinar status geral
        if self.count_divergencias_ibs > 0 or self.count_divergencias_cbs > 0:
            self.status_geral = ValidationStatus.DIVERGENTE
        elif self.count_sem_tag_ibs == self.total_itens and self.count_sem_tag_cbs == self.total_itens:
            self.status_geral = ValidationStatus.SEM_TAG
        else:
            self.status_geral = ValidationStatus.OK


@dataclass
class ErrorRecord:
    """Registro de erro no processamento de um XML."""
    arquivo: str
    error_type: str
    error_message: str
    timestamp: datetime = field(default_factory=datetime.now)
