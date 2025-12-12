"""
Calculadora de base de IBS/CBS conforme fórmula configurável.
"""

import logging
from decimal import Decimal
from typing import List

from .models import Item, NFe
from .config import Config, IncludeComponentsConfig

logger = logging.getLogger(__name__)


class IBSCBSCalculator:
    """Calcula base de IBS e CBS para itens de NF-e."""
    
    def __init__(self, config: Config):
        """
        Inicializa calculadora.
        
        Args:
            config: Configuração do sistema
        """
        self.config = config
        self.components = config.include_components
    
    def calculate_nfe(self, nfe: NFe):
        """
        Calcula base de IBS/CBS para todos os itens da NF-e.
        Atualiza os campos base_calculada_ibs e base_calculada_cbs de cada item.
        
        Args:
            nfe: Objeto NFe com itens
        """
        for item in nfe.itens:
            self.calculate_item(item)
    
    def calculate_item(self, item: Item):
        """
        Calcula base de IBS e CBS para um item específico.
        
        A fórmula padrão é:
        Base = vProd 
             + (vFrete se habilitado)
             + (vSeg se habilitado)
             + (vOutro se habilitado)
             - (vDesc sempre subtrai)
             + (vIPI se habilitado)
             + (vII se habilitado)
             + (vICMSST se habilitado)
             + (vFCPST se habilitado)
             + (vPIS se habilitado)
             + (vCOFINS se habilitado)
        
        Args:
            item: Objeto Item a calcular
        """
        base = item.vProd
        
        # Componentes do produto
        if self.components.freight:
            base += item.vFrete
        
        if self.components.insurance:
            base += item.vSeg
        
        if self.components.other:
            base += item.vOutro
        
        # Desconto sempre subtrai (se configurado)
        if self.components.discount:
            base -= item.vDesc
        
        # Tributos opcionais
        if self.components.ipi:
            base += item.tributos.vIPI
        
        if self.components.ii:
            base += item.tributos.vII
        
        if self.components.icms_st:
            base += item.tributos.vICMSST
        
        if self.components.fcp_st:
            base += item.tributos.vFCPST
        
        if self.components.pis:
            base += item.tributos.vPIS
        
        if self.components.cofins:
            base += item.tributos.vCOFINS
        
        # Garantir que base não seja negativa
        if base < Decimal("0"):
            logger.warning(
                f"Base calculada negativa no item {item.nItem} "
                f"(cProd={item.cProd}): {base}. Mantendo valor calculado."
            )
        
        # Para IBS e CBS, a base é a mesma (pode variar no futuro)
        item.base_calculada_ibs = base
        item.base_calculada_cbs = base
    
    def calculate_total_base(self, itens: List[Item]) -> tuple[Decimal, Decimal]:
        """
        Calcula totais de base IBS e CBS.
        
        Args:
            itens: Lista de itens
        
        Returns:
            Tupla (total_base_ibs, total_base_cbs)
        """
        total_ibs = sum(
            (item.base_calculada_ibs for item in itens if item.base_calculada_ibs),
            Decimal("0")
        )
        
        total_cbs = sum(
            (item.base_calculada_cbs for item in itens if item.base_calculada_cbs),
            Decimal("0")
        )
        
        return total_ibs, total_cbs
    
    def get_formula_description(self) -> str:
        """
        Retorna descrição textual da fórmula de cálculo.
        
        Returns:
            String descrevendo a fórmula
        """
        components = ["vProd"]
        
        if self.components.freight:
            components.append("vFrete")
        if self.components.insurance:
            components.append("vSeg")
        if self.components.other:
            components.append("vOutro")
        if self.components.discount:
            components.append("-vDesc")
        if self.components.ipi:
            components.append("vIPI")
        if self.components.ii:
            components.append("vII")
        if self.components.icms_st:
            components.append("vICMSST")
        if self.components.fcp_st:
            components.append("vFCPST")
        if self.components.pis:
            components.append("vPIS")
        if self.components.cofins:
            components.append("vCOFINS")
        
        return "Base = " + " + ".join(components)
