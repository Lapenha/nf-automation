"""
Testes do comparador.
"""

import unittest
from decimal import Decimal

from nfe_validator.comparator import IBSCBSComparator
from nfe_validator.config import Config
from nfe_validator.models import Item, IBSCBSData, ValidationStatus


class TestIBSCBSComparator(unittest.TestCase):
    """Testes do comparador."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.config = Config()
        self.config.tolerance.absolute = 0.05
        self.config.tolerance.percentage = 0.1
        self.comparator = IBSCBSComparator(self.config)
    
    def test_compare_within_absolute_tolerance(self):
        """Testa comparação dentro da tolerância absoluta."""
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("1"),
            vUnCom=Decimal("1000"),
            vProd=Decimal("1000.00"),
            base_calculada_ibs=Decimal("1000.03"),  # Diferença de 0.03
            base_calculada_cbs=Decimal("1000.03"),
            ibs_xml=IBSCBSData(
                vBC=Decimal("1000.00"),
                pAliq=Decimal("0.5"),
                vTributo=Decimal("5.00"),
                found=True,
            ),
            cbs_xml=IBSCBSData(found=False),
        )
        
        result = self.comparator.compare_item(item)
        
        # Diferença de 0.03 está dentro da tolerância absoluta de 0.05
        self.assertFalse(result.diverge_base_ibs)
        self.assertEqual(result.status_ibs, ValidationStatus.OK)
    
    def test_compare_outside_tolerance(self):
        """Testa comparação fora da tolerância."""
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("1"),
            vUnCom=Decimal("1000"),
            vProd=Decimal("1000.00"),
            base_calculada_ibs=Decimal("1010.00"),  # Diferença de 10.00
            base_calculada_cbs=Decimal("1010.00"),
            ibs_xml=IBSCBSData(
                vBC=Decimal("1000.00"),
                pAliq=Decimal("0.5"),
                vTributo=Decimal("5.00"),
                found=True,
            ),
            cbs_xml=IBSCBSData(found=False),
        )
        
        result = self.comparator.compare_item(item)
        
        # Diferença de 10.00 está fora da tolerância
        self.assertTrue(result.diverge_base_ibs)
        self.assertEqual(result.status_ibs, ValidationStatus.DIVERGENTE)
    
    def test_compare_percentage_tolerance(self):
        """Testa tolerância percentual."""
        # Para valor grande, tolerância percentual é maior
        # Valor de referência: 10000
        # Tolerância absoluta: 0.05
        # Tolerância percentual: 0.1% de 10000 = 10.00
        # Usa a maior: 10.00
        
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("1"),
            vUnCom=Decimal("10000"),
            vProd=Decimal("10000.00"),
            base_calculada_ibs=Decimal("10008.00"),  # Diferença de 8.00
            base_calculada_cbs=Decimal("10008.00"),
            ibs_xml=IBSCBSData(
                vBC=Decimal("10000.00"),
                pAliq=Decimal("0.5"),
                vTributo=Decimal("50.00"),
                found=True,
            ),
            cbs_xml=IBSCBSData(found=False),
        )
        
        result = self.comparator.compare_item(item)
        
        # Diferença de 8.00 está dentro de 10.00 (0.1% de 10000)
        self.assertFalse(result.diverge_base_ibs)
        self.assertEqual(result.status_ibs, ValidationStatus.OK)
    
    def test_compare_without_xml_data(self):
        """Testa comparação quando não há dados no XML."""
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("1"),
            vUnCom=Decimal("1000"),
            vProd=Decimal("1000.00"),
            base_calculada_ibs=Decimal("1000.00"),
            base_calculada_cbs=Decimal("1000.00"),
            ibs_xml=IBSCBSData(found=False),
            cbs_xml=IBSCBSData(found=False),
        )
        
        result = self.comparator.compare_item(item)
        
        # Deve marcar como SEM_TAG
        self.assertEqual(result.status_ibs, ValidationStatus.SEM_TAG)
        self.assertEqual(result.status_cbs, ValidationStatus.SEM_TAG)
        self.assertEqual(result.status_geral, ValidationStatus.SEM_TAG)
    
    def test_compare_valor_tributo(self):
        """Testa comparação do valor do tributo calculado vs informado."""
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("1"),
            vUnCom=Decimal("1000"),
            vProd=Decimal("1000.00"),
            base_calculada_ibs=Decimal("1000.00"),
            base_calculada_cbs=Decimal("1000.00"),
            ibs_xml=IBSCBSData(
                vBC=Decimal("1000.00"),
                pAliq=Decimal("0.5"),  # 0.5%
                vTributo=Decimal("5.00"),  # 1000 * 0.5% = 5.00
                found=True,
            ),
            cbs_xml=IBSCBSData(found=False),
        )
        
        result = self.comparator.compare_item(item)
        
        # Base OK e valor OK
        self.assertFalse(result.diverge_base_ibs)
        self.assertFalse(result.diverge_valor_ibs)
        self.assertEqual(result.status_ibs, ValidationStatus.OK)
    
    def test_compare_valor_tributo_divergente(self):
        """Testa comparação com valor do tributo divergente."""
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("1"),
            vUnCom=Decimal("1000"),
            vProd=Decimal("1000.00"),
            base_calculada_ibs=Decimal("1000.00"),
            base_calculada_cbs=Decimal("1000.00"),
            ibs_xml=IBSCBSData(
                vBC=Decimal("1000.00"),
                pAliq=Decimal("0.5"),  # 0.5%
                vTributo=Decimal("10.00"),  # Informado errado (deveria ser 5.00)
                found=True,
            ),
            cbs_xml=IBSCBSData(found=False),
        )
        
        result = self.comparator.compare_item(item)
        
        # Valor calculado: 1000 * 0.5% = 5.00
        # Valor informado: 10.00
        # Delta: -5.00 (fora da tolerância)
        self.assertTrue(result.diverge_valor_ibs)
        self.assertEqual(result.status_ibs, ValidationStatus.DIVERGENTE)


if __name__ == "__main__":
    unittest.main()
