"""
Testes básicos do parser.
"""

import unittest
from decimal import Decimal
from pathlib import Path
from datetime import datetime
from lxml import etree

from nfe_validator.parser import NFeParser
from nfe_validator.config import Config


class TestNFeParser(unittest.TestCase):
    """Testes do parser de NF-e."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.config = Config()
        self.parser = NFeParser(self.config)
    
    def test_parse_basic_nfe_structure(self):
        """Testa parse de estrutura básica de NF-e."""
        # XML mínimo de teste
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
    <NFe>
        <infNFe Id="NFe12345678901234567890123456789012345678901234">
            <ide>
                <nNF>123</nNF>
                <serie>1</serie>
                <dhEmi>2025-12-12T10:00:00-03:00</dhEmi>
            </ide>
            <emit>
                <CNPJ>12345678000190</CNPJ>
                <xNome>Empresa Teste LTDA</xNome>
                <enderEmit>
                    <UF>SP</UF>
                </enderEmit>
            </emit>
            <dest>
                <CNPJ>98765432000180</CNPJ>
                <xNome>Cliente Teste</xNome>
                <enderDest>
                    <UF>RJ</UF>
                </enderDest>
            </dest>
            <total>
                <ICMSTot>
                    <vNF>1000.00</vNF>
                    <vProd>900.00</vProd>
                </ICMSTot>
            </total>
            <det nItem="1">
                <prod>
                    <cProd>PROD001</cProd>
                    <xProd>Produto Teste</xProd>
                    <NCM>12345678</NCM>
                    <CFOP>5102</CFOP>
                    <uCom>UN</uCom>
                    <qCom>10.00</qCom>
                    <vUnCom>90.00</vUnCom>
                    <vProd>900.00</vProd>
                </prod>
                <imposto>
                </imposto>
            </det>
        </infNFe>
    </NFe>
</nfeProc>"""
        
        # Salvar temporariamente
        temp_file = Path("test_nfe.xml")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        try:
            # Parse
            nfe = self.parser.parse_file(temp_file)
            
            # Validações
            self.assertIsNotNone(nfe)
            self.assertEqual(nfe.nNF, "123")
            self.assertEqual(nfe.serie, "1")
            self.assertEqual(nfe.emit_CNPJ, "12345678000190")
            self.assertEqual(nfe.emit_xNome, "Empresa Teste LTDA")
            self.assertEqual(nfe.dest_CNPJ, "98765432000180")
            self.assertEqual(nfe.vNF, Decimal("1000.00"))
            self.assertEqual(len(nfe.itens), 1)
            
            # Validar item
            item = nfe.itens[0]
            self.assertEqual(item.nItem, 1)
            self.assertEqual(item.cProd, "PROD001")
            self.assertEqual(item.xProd, "Produto Teste")
            self.assertEqual(item.vProd, Decimal("900.00"))
            
        finally:
            # Limpar
            if temp_file.exists():
                temp_file.unlink()
    
    def test_extract_ibs_cbs_from_xml(self):
        """Testa extração de IBS/CBS do XML."""
        # XML com IBS/CBS
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
    <NFe>
        <infNFe Id="NFe12345678901234567890123456789012345678901234">
            <ide>
                <nNF>456</nNF>
                <serie>1</serie>
                <dhEmi>2025-12-12T10:00:00-03:00</dhEmi>
            </ide>
            <emit>
                <CNPJ>12345678000190</CNPJ>
                <xNome>Empresa Teste</xNome>
                <enderEmit><UF>SP</UF></enderEmit>
            </emit>
            <total>
                <ICMSTot>
                    <vNF>1100.00</vNF>
                    <vProd>1000.00</vProd>
                </ICMSTot>
            </total>
            <det nItem="1">
                <prod>
                    <cProd>PROD002</cProd>
                    <xProd>Produto com IBS/CBS</xProd>
                    <NCM>12345678</NCM>
                    <CFOP>5102</CFOP>
                    <uCom>UN</uCom>
                    <qCom>1.00</qCom>
                    <vUnCom>1000.00</vUnCom>
                    <vProd>1000.00</vProd>
                </prod>
                <imposto>
                    <IBS>
                        <vBC>1000.00</vBC>
                        <pIBS>0.50</pIBS>
                        <vIBS>5.00</vIBS>
                    </IBS>
                    <CBS>
                        <vBC>1000.00</vBC>
                        <pCBS>1.50</pCBS>
                        <vCBS>15.00</vCBS>
                    </CBS>
                </imposto>
            </det>
        </infNFe>
    </NFe>
</nfeProc>"""
        
        temp_file = Path("test_nfe_ibs_cbs.xml")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        try:
            nfe = self.parser.parse_file(temp_file)
            
            self.assertIsNotNone(nfe)
            self.assertEqual(len(nfe.itens), 1)
            
            item = nfe.itens[0]
            
            # Validar IBS
            self.assertTrue(item.ibs_xml.found)
            self.assertEqual(item.ibs_xml.vBC, Decimal("1000.00"))
            self.assertEqual(item.ibs_xml.pAliq, Decimal("0.50"))
            self.assertEqual(item.ibs_xml.vTributo, Decimal("5.00"))
            
            # Validar CBS
            self.assertTrue(item.cbs_xml.found)
            self.assertEqual(item.cbs_xml.vBC, Decimal("1000.00"))
            self.assertEqual(item.cbs_xml.pAliq, Decimal("1.50"))
            self.assertEqual(item.cbs_xml.vTributo, Decimal("15.00"))
            
        finally:
            if temp_file.exists():
                temp_file.unlink()


if __name__ == "__main__":
    unittest.main()
