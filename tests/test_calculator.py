"""
Testes da calculadora de base IBS/CBS.
"""

import unittest
from decimal import Decimal

from nfe_validator.calculator import IBSCBSCalculator
from nfe_validator.config import Config
from nfe_validator.models import Item, Tributos


class TestIBSCBSCalculator(unittest.TestCase):
    """Testes da calculadora."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.config = Config()
        self.calculator = IBSCBSCalculator(self.config)
    
    def test_calculate_base_simple(self):
        """Testa cálculo de base simples (apenas vProd)."""
        # Desabilitar componentes opcionais
        self.config.include_components.freight = False
        self.config.include_components.insurance = False
        self.config.include_components.other = False
        self.config.include_components.discount = False
        
        self.calculator = IBSCBSCalculator(self.config)
        
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("10"),
            vUnCom=Decimal("100"),
            vProd=Decimal("1000.00"),
        )
        
        self.calculator.calculate_item(item)
        
        # Base deve ser igual a vProd
        self.assertEqual(item.base_calculada_ibs, Decimal("1000.00"))
        self.assertEqual(item.base_calculada_cbs, Decimal("1000.00"))
    
    def test_calculate_base_with_components(self):
        """Testa cálculo de base com componentes adicionais."""
        # Habilitar todos os componentes
        self.config.include_components.freight = True
        self.config.include_components.insurance = True
        self.config.include_components.other = True
        self.config.include_components.discount = True
        
        self.calculator = IBSCBSCalculator(self.config)
        
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("10"),
            vUnCom=Decimal("100"),
            vProd=Decimal("1000.00"),
            vFrete=Decimal("50.00"),
            vSeg=Decimal("10.00"),
            vOutro=Decimal("5.00"),
            vDesc=Decimal("20.00"),
        )
        
        self.calculator.calculate_item(item)
        
        # Base = 1000 + 50 + 10 + 5 - 20 = 1045
        expected = Decimal("1045.00")
        self.assertEqual(item.base_calculada_ibs, expected)
        self.assertEqual(item.base_calculada_cbs, expected)
    
    def test_calculate_base_with_tributes(self):
        """Testa cálculo de base com tributos opcionais."""
        # Habilitar tributos
        self.config.include_components.freight = False
        self.config.include_components.insurance = False
        self.config.include_components.other = False
        self.config.include_components.discount = False
        self.config.include_components.ipi = True
        self.config.include_components.icms_st = True
        
        self.calculator = IBSCBSCalculator(self.config)
        
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("10"),
            vUnCom=Decimal("100"),
            vProd=Decimal("1000.00"),
            tributos=Tributos(
                vIPI=Decimal("100.00"),
                vICMSST=Decimal("50.00"),
            ),
        )
        
        self.calculator.calculate_item(item)
        
        # Base = 1000 + 100 (IPI) + 50 (ICMS ST) = 1150
        expected = Decimal("1150.00")
        self.assertEqual(item.base_calculada_ibs, expected)
        self.assertEqual(item.base_calculada_cbs, expected)
    
    def test_calculate_base_with_discount_only(self):
        """Testa cálculo de base com desconto."""
        self.config.include_components.freight = False
        self.config.include_components.insurance = False
        self.config.include_components.other = False
        self.config.include_components.discount = True
        
        self.calculator = IBSCBSCalculator(self.config)
        
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("10"),
            vUnCom=Decimal("100"),
            vProd=Decimal("1000.00"),
            vDesc=Decimal("100.00"),
        )
        
        self.calculator.calculate_item(item)
        
        # Base = 1000 - 100 = 900
        expected = Decimal("900.00")
        self.assertEqual(item.base_calculada_ibs, expected)
        self.assertEqual(item.base_calculada_cbs, expected)
    
    def test_calculate_negative_base_warning(self):
        """Testa comportamento com base negativa (aviso, mas mantém valor)."""
        self.config.include_components.discount = True
        
        self.calculator = IBSCBSCalculator(self.config)
        
        item = Item(
            nItem=1,
            cProd="PROD001",
            xProd="Produto Teste",
            NCM="12345678",
            CFOP="5102",
            uCom="UN",
            qCom=Decimal("10"),
            vUnCom=Decimal("100"),
            vProd=Decimal("100.00"),
            vDesc=Decimal("200.00"),  # Desconto maior que produto
        )
        
        self.calculator.calculate_item(item)
        
        # Base negativa deve ser mantida (com warning no log)
        self.assertEqual(item.base_calculada_ibs, Decimal("-100.00"))


if __name__ == "__main__":
    unittest.main()
