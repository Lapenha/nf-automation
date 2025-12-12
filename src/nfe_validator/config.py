"""
Sistema de configuração do validador.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class XPathConfig:
    """Configuração de XPaths para busca de tributos."""
    base_paths: List[str] = field(default_factory=list)
    rate_paths: List[str] = field(default_factory=list)
    value_paths: List[str] = field(default_factory=list)


@dataclass
class IBSCBSXPathsConfig:
    """XPaths para IBS e CBS."""
    ibs: XPathConfig = field(default_factory=XPathConfig)
    cbs: XPathConfig = field(default_factory=XPathConfig)


@dataclass
class ToleranceConfig:
    """Configuração de tolerâncias."""
    absolute: float = 0.05  # Tolerância absoluta em reais
    percentage: float = 0.1  # Tolerância percentual (0.1 = 0.1%)


@dataclass
class IncludeComponentsConfig:
    """Flags para inclusão de componentes na base de cálculo."""
    freight: bool = True  # vFrete
    insurance: bool = True  # vSeg
    other: bool = True  # vOutro
    discount: bool = True  # vDesc (sempre subtrai)
    ipi: bool = False  # vIPI
    ii: bool = False  # vII
    icms_st: bool = False  # vICMSST
    fcp_st: bool = False  # vFCPST
    pis: bool = False  # vPIS
    cofins: bool = False  # vCOFINS


@dataclass
class ExecutionConfig:
    """Configuração de execução."""
    only_divergences: bool = False  # Processar apenas divergentes
    max_files: Optional[int] = None  # Limite de arquivos (None = todos)
    workers: int = 1  # Número de workers para processamento paralelo
    debug: bool = False  # Modo debug
    recurse_subfolders: bool = True  # Buscar em subpastas


@dataclass
class Config:
    """Configuração principal do validador."""
    input_dir: str = "./xmls"
    output_dir: str = "./output"
    
    tolerance: ToleranceConfig = field(default_factory=ToleranceConfig)
    include_components: IncludeComponentsConfig = field(default_factory=IncludeComponentsConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
    xpaths: IBSCBSXPathsConfig = field(default_factory=IBSCBSXPathsConfig)
    
    def __post_init__(self):
        """Inicializa XPaths padrão se não fornecidos."""
        if not self.xpaths.ibs.base_paths:
            self.xpaths.ibs.base_paths = [
                ".//*[local-name()='IBS']/*[local-name()='vBC']",
                ".//*[local-name()='vBCIBS']",
                ".//*[local-name()='IBS']/*[local-name()='vBCTrib']",
            ]
        
        if not self.xpaths.ibs.rate_paths:
            self.xpaths.ibs.rate_paths = [
                ".//*[local-name()='IBS']/*[local-name()='pIBS']",
                ".//*[local-name()='pAliqIBS']",
                ".//*[local-name()='IBS']/*[local-name()='pAliq']",
            ]
        
        if not self.xpaths.ibs.value_paths:
            self.xpaths.ibs.value_paths = [
                ".//*[local-name()='IBS']/*[local-name()='vIBS']",
                ".//*[local-name()='vIBS']",
                ".//*[local-name()='IBS']/*[local-name()='vTrib']",
            ]
        
        if not self.xpaths.cbs.base_paths:
            self.xpaths.cbs.base_paths = [
                ".//*[local-name()='CBS']/*[local-name()='vBC']",
                ".//*[local-name()='vBCCBS']",
                ".//*[local-name()='CBS']/*[local-name()='vBCTrib']",
            ]
        
        if not self.xpaths.cbs.rate_paths:
            self.xpaths.cbs.rate_paths = [
                ".//*[local-name()='CBS']/*[local-name()='pCBS']",
                ".//*[local-name()='pAliqCBS']",
                ".//*[local-name()='CBS']/*[local-name()='pAliq']",
            ]
        
        if not self.xpaths.cbs.value_paths:
            self.xpaths.cbs.value_paths = [
                ".//*[local-name()='CBS']/*[local-name()='vCBS']",
                ".//*[local-name()='vCBS']",
                ".//*[local-name()='CBS']/*[local-name()='vTrib']",
            ]
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "Config":
        """Carrega configuração de um arquivo YAML."""
        path = Path(yaml_path)
        
        if not path.exists():
            logger.warning(f"Arquivo de configuração não encontrado: {yaml_path}. Usando padrões.")
            return cls()
        
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Cria Config a partir de dicionário."""
        config = cls()
        
        # Diretórios
        config.input_dir = data.get("input_dir", config.input_dir)
        config.output_dir = data.get("output_dir", config.output_dir)
        
        # Tolerância
        if "tolerance" in data:
            tol = data["tolerance"]
            config.tolerance.absolute = tol.get("absolute", config.tolerance.absolute)
            config.tolerance.percentage = tol.get("percentage", config.tolerance.percentage)
        
        # Componentes
        if "include_components" in data:
            comp = data["include_components"]
            config.include_components.freight = comp.get("freight", config.include_components.freight)
            config.include_components.insurance = comp.get("insurance", config.include_components.insurance)
            config.include_components.other = comp.get("other", config.include_components.other)
            config.include_components.discount = comp.get("discount", config.include_components.discount)
            config.include_components.ipi = comp.get("ipi", config.include_components.ipi)
            config.include_components.ii = comp.get("ii", config.include_components.ii)
            config.include_components.icms_st = comp.get("icms_st", config.include_components.icms_st)
            config.include_components.fcp_st = comp.get("fcp_st", config.include_components.fcp_st)
            config.include_components.pis = comp.get("pis", config.include_components.pis)
            config.include_components.cofins = comp.get("cofins", config.include_components.cofins)
        
        # Execução
        if "execution" in data:
            exec_cfg = data["execution"]
            config.execution.only_divergences = exec_cfg.get("only_divergences", config.execution.only_divergences)
            config.execution.max_files = exec_cfg.get("max_files", config.execution.max_files)
            config.execution.workers = exec_cfg.get("workers", config.execution.workers)
            config.execution.debug = exec_cfg.get("debug", config.execution.debug)
            config.execution.recurse_subfolders = exec_cfg.get("recurse_subfolders", config.execution.recurse_subfolders)
        
        # XPaths
        if "xpaths" in data:
            xpaths_data = data["xpaths"]
            
            if "ibs" in xpaths_data:
                ibs = xpaths_data["ibs"]
                if "base_paths" in ibs:
                    config.xpaths.ibs.base_paths = ibs["base_paths"]
                if "rate_paths" in ibs:
                    config.xpaths.ibs.rate_paths = ibs["rate_paths"]
                if "value_paths" in ibs:
                    config.xpaths.ibs.value_paths = ibs["value_paths"]
            
            if "cbs" in xpaths_data:
                cbs = xpaths_data["cbs"]
                if "base_paths" in cbs:
                    config.xpaths.cbs.base_paths = cbs["base_paths"]
                if "rate_paths" in cbs:
                    config.xpaths.cbs.rate_paths = cbs["rate_paths"]
                if "value_paths" in cbs:
                    config.xpaths.cbs.value_paths = cbs["value_paths"]
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte Config para dicionário."""
        return {
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
            "tolerance": {
                "absolute": self.tolerance.absolute,
                "percentage": self.tolerance.percentage,
            },
            "include_components": {
                "freight": self.include_components.freight,
                "insurance": self.include_components.insurance,
                "other": self.include_components.other,
                "discount": self.include_components.discount,
                "ipi": self.include_components.ipi,
                "ii": self.include_components.ii,
                "icms_st": self.include_components.icms_st,
                "fcp_st": self.include_components.fcp_st,
                "pis": self.include_components.pis,
                "cofins": self.include_components.cofins,
            },
            "execution": {
                "only_divergences": self.execution.only_divergences,
                "max_files": self.execution.max_files,
                "workers": self.execution.workers,
                "debug": self.execution.debug,
                "recurse_subfolders": self.execution.recurse_subfolders,
            },
            "xpaths": {
                "ibs": {
                    "base_paths": self.xpaths.ibs.base_paths,
                    "rate_paths": self.xpaths.ibs.rate_paths,
                    "value_paths": self.xpaths.ibs.value_paths,
                },
                "cbs": {
                    "base_paths": self.xpaths.cbs.base_paths,
                    "rate_paths": self.xpaths.cbs.rate_paths,
                    "value_paths": self.xpaths.cbs.value_paths,
                },
            },
        }
    
    def save_to_yaml(self, yaml_path: str):
        """Salva configuração em arquivo YAML."""
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        logger.info(f"Configuração salva em: {yaml_path}")


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Carrega configuração de um arquivo YAML ou retorna configuração padrão.
    
    Args:
        config_path: Caminho para arquivo de configuração. Se None, busca por 
                    config.yaml ou config.example.yaml no diretório atual.
    
    Returns:
        Config: Objeto de configuração
    """
    if config_path is None:
        # Busca por config.yaml ou config.example.yaml
        if Path("config.yaml").exists():
            config_path = "config.yaml"
        elif Path("config.example.yaml").exists():
            config_path = "config.example.yaml"
        else:
            logger.warning("Nenhum arquivo de configuração encontrado. Usando configuração padrão.")
            return Config()
    
    try:
        return Config.from_yaml(config_path)
    except Exception as e:
        logger.warning(f"Erro ao carregar configuração: {e}. Usando configuração padrão.")
        return Config()
