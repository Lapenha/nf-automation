"""
NF-e IBS/CBS Validator
Validação em massa de XMLs de NF-e com foco em IBS/CBS (Reforma Tributária)
"""

__version__ = "1.0.0"
__author__ = "Murilo Alapenha Soares"

from .models import (
    NFe,
    Item,
    Tributos,
    IBSCBSData,
    ComparisonResult,
    ItemComparisonResult,
    ValidationStatus,
    ErrorRecord,
)
from .config import Config
from .parser import NFeParser
from .calculator import IBSCBSCalculator
from .comparator import IBSCBSComparator
from .report import ExcelReportGenerator

__all__ = [
    "NFe",
    "Item",
    "Tributos",
    "IBSCBSData",
    "ComparisonResult",
    "ItemComparisonResult",
    "ValidationStatus",
    "ErrorRecord",
    "Config",
    "NFeParser",
    "IBSCBSCalculator",
    "IBSCBSComparator",
    "ExcelReportGenerator",
]
