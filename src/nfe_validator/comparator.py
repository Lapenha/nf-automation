"""
Comparador de valores calculados vs. informados no XML com tolerância.
"""

import logging
from decimal import Decimal
from typing import Optional

from .models import (
    NFe,
    Item,
    ComparisonResult,
    ItemComparisonResult,
    ValidationStatus,
)
from .config import Config, ToleranceConfig

logger = logging.getLogger(__name__)


class IBSCBSComparator:
    """Compara valores calculados com valores informados no XML."""
    
    def __init__(self, config: Config):
        """
        Inicializa comparador.
        
        Args:
            config: Configuração do sistema
        """
        self.config = config
        self.tolerance = config.tolerance
    
    def compare_nfe(self, nfe: NFe) -> ComparisonResult:
        """
        Compara todos os itens de uma NF-e.
        
        Args:
            nfe: NF-e com itens calculados
        
        Returns:
            Resultado da comparação
        """
        result = ComparisonResult(nfe=nfe)
        
        for item in nfe.itens:
            item_result = self.compare_item(item)
            result.itens_resultado.append(item_result)
        
        # Calcular totais e contadores
        result.calcular_totais()
        
        return result
    
    def compare_item(self, item: Item) -> ItemComparisonResult:
        """
        Compara um item específico.
        
        Args:
            item: Item com base calculada e dados XML
        
        Returns:
            Resultado da comparação do item
        """
        # Inicializar resultado
        result = ItemComparisonResult(
            nItem=item.nItem,
            cProd=item.cProd,
            xProd=item.xProd,
            base_calc_ibs=item.base_calculada_ibs or Decimal("0"),
            base_calc_cbs=item.base_calculada_cbs or Decimal("0"),
            base_xml_ibs=item.ibs_xml.vBC,
            aliq_xml_ibs=item.ibs_xml.pAliq,
            valor_xml_ibs=item.ibs_xml.vTributo,
            base_xml_cbs=item.cbs_xml.vBC,
            aliq_xml_cbs=item.cbs_xml.pAliq,
            valor_xml_cbs=item.cbs_xml.vTributo,
        )
        
        # Comparar IBS
        result.status_ibs = self._compare_tributo(
            base_calculada=result.base_calc_ibs,
            base_xml=result.base_xml_ibs,
            aliq_xml=result.aliq_xml_ibs,
            valor_xml=result.valor_xml_ibs,
            found=item.ibs_xml.found,
            result=result,
            tributo_tipo="IBS",
        )
        
        # Comparar CBS
        result.status_cbs = self._compare_tributo(
            base_calculada=result.base_calc_cbs,
            base_xml=result.base_xml_cbs,
            aliq_xml=result.aliq_xml_cbs,
            valor_xml=result.valor_xml_cbs,
            found=item.cbs_xml.found,
            result=result,
            tributo_tipo="CBS",
        )
        
        # Status geral do item
        if result.status_ibs == ValidationStatus.DIVERGENTE or result.status_cbs == ValidationStatus.DIVERGENTE:
            result.status_geral = ValidationStatus.DIVERGENTE
        elif result.status_ibs == ValidationStatus.SEM_TAG and result.status_cbs == ValidationStatus.SEM_TAG:
            result.status_geral = ValidationStatus.SEM_TAG
        else:
            result.status_geral = ValidationStatus.OK
        
        return result
    
    def _compare_tributo(
        self,
        base_calculada: Decimal,
        base_xml: Optional[Decimal],
        aliq_xml: Optional[Decimal],
        valor_xml: Optional[Decimal],
        found: bool,
        result: ItemComparisonResult,
        tributo_tipo: str,
    ) -> ValidationStatus:
        """
        Compara um tributo específico (IBS ou CBS).
        
        Args:
            base_calculada: Base calculada
            base_xml: Base informada no XML
            aliq_xml: Alíquota informada no XML
            valor_xml: Valor informado no XML
            found: Se foi encontrado no XML
            result: Objeto resultado para atualizar deltas
            tributo_tipo: "IBS" ou "CBS"
        
        Returns:
            Status de validação
        """
        # Se não encontrou no XML
        if not found or (base_xml is None and aliq_xml is None and valor_xml is None):
            return ValidationStatus.SEM_TAG
        
        status = ValidationStatus.OK
        
        # Comparar base de cálculo
        if base_xml is not None:
            delta_base = base_calculada - base_xml
            
            if tributo_tipo == "IBS":
                result.delta_base_ibs = delta_base
                result.diverge_base_ibs = not self._within_tolerance(delta_base, base_xml)
                if result.diverge_base_ibs:
                    status = ValidationStatus.DIVERGENTE
            else:  # CBS
                result.delta_base_cbs = delta_base
                result.diverge_base_cbs = not self._within_tolerance(delta_base, base_xml)
                if result.diverge_base_cbs:
                    status = ValidationStatus.DIVERGENTE
        
        # Comparar valor do tributo (se houver alíquota e valor)
        if aliq_xml is not None and valor_xml is not None:
            # Calcular valor esperado: base_calculada * alíquota / 100
            valor_calculado = base_calculada * aliq_xml / Decimal("100")
            delta_valor = valor_calculado - valor_xml
            
            if tributo_tipo == "IBS":
                result.delta_valor_ibs = delta_valor
                result.diverge_valor_ibs = not self._within_tolerance(delta_valor, valor_xml)
                if result.diverge_valor_ibs:
                    status = ValidationStatus.DIVERGENTE
            else:  # CBS
                result.delta_valor_cbs = delta_valor
                result.diverge_valor_cbs = not self._within_tolerance(delta_valor, valor_xml)
                if result.diverge_valor_cbs:
                    status = ValidationStatus.DIVERGENTE
        
        return status
    
    def _within_tolerance(self, delta: Decimal, reference_value: Decimal) -> bool:
        """
        Verifica se a diferença está dentro da tolerância.
        
        Regra: divergência quando |delta| > max(tol_abs, tol_pct * |valor_referência|)
        
        Args:
            delta: Diferença entre calculado e informado
            reference_value: Valor de referência (informado no XML)
        
        Returns:
            True se dentro da tolerância
        """
        delta_abs = abs(delta)
        reference_abs = abs(reference_value)
        
        # Tolerância absoluta
        tol_abs = Decimal(str(self.tolerance.absolute))
        
        # Tolerância percentual
        tol_pct = Decimal(str(self.tolerance.percentage)) / Decimal("100")
        tol_pct_value = tol_pct * reference_abs
        
        # Tolerância efetiva é o maior valor
        tolerance_threshold = max(tol_abs, tol_pct_value)
        
        return delta_abs <= tolerance_threshold
    
    def get_divergence_summary(self, result: ComparisonResult) -> dict:
        """
        Retorna resumo de divergências de uma NF-e.
        
        Args:
            result: Resultado da comparação
        
        Returns:
            Dicionário com resumo
        """
        divergent_items = [
            item for item in result.itens_resultado
            if item.status_geral == ValidationStatus.DIVERGENTE
        ]
        
        return {
            "total_itens": result.total_itens,
            "divergencias_ibs": result.count_divergencias_ibs,
            "divergencias_cbs": result.count_divergencias_cbs,
            "sem_tag_ibs": result.count_sem_tag_ibs,
            "sem_tag_cbs": result.count_sem_tag_cbs,
            "itens_divergentes": len(divergent_items),
            "status_geral": result.status_geral.value,
        }
