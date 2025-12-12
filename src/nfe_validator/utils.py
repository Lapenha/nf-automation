"""
Funções utilitárias.
"""

import logging
from decimal import Decimal, InvalidOperation
from typing import Optional, Any
from lxml import etree


def setup_logger(name: str, level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Configura logger com formatação padrão."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicação de handlers
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (opcional)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def to_decimal(value: Any, default: Decimal = Decimal("0")) -> Decimal:
    """
    Converte valor para Decimal de forma segura.
    
    Args:
        value: Valor a converter (str, int, float, Decimal)
        default: Valor padrão em caso de erro
    
    Returns:
        Decimal convertido ou valor padrão
    """
    if value is None or value == "":
        return default
    
    if isinstance(value, Decimal):
        return value
    
    try:
        # Remove espaços e trata vírgula como ponto
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return default


def extract_text_safe(element: Optional[etree._Element], xpath: str, default: str = "") -> str:
    """
    Extrai texto de elemento XML de forma segura.
    
    Args:
        element: Elemento XML
        xpath: XPath relativo
        default: Valor padrão se não encontrar
    
    Returns:
        Texto extraído ou valor padrão
    """
    if element is None:
        return default
    
    try:
        result = element.xpath(xpath)
        if result and len(result) > 0:
            if isinstance(result[0], str):
                return result[0].strip()
            elif hasattr(result[0], "text"):
                return (result[0].text or "").strip()
        return default
    except Exception:
        return default


def extract_decimal_safe(element: Optional[etree._Element], xpath: str, default: Decimal = Decimal("0")) -> Decimal:
    """
    Extrai valor decimal de elemento XML de forma segura.
    
    Args:
        element: Elemento XML
        xpath: XPath relativo
        default: Valor padrão se não encontrar
    
    Returns:
        Decimal extraído ou valor padrão
    """
    text = extract_text_safe(element, xpath, "")
    return to_decimal(text, default)


def find_with_xpaths(element: Optional[etree._Element], xpath_list: list[str]) -> Optional[str]:
    """
    Tenta encontrar valor usando lista de XPaths alternativos.
    
    Args:
        element: Elemento XML onde buscar
        xpath_list: Lista de XPaths para tentar
    
    Returns:
        Primeiro valor encontrado ou None
    """
    if element is None:
        return None
    
    for xpath in xpath_list:
        try:
            result = element.xpath(xpath)
            if result and len(result) > 0:
                if isinstance(result[0], str):
                    text = result[0].strip()
                elif hasattr(result[0], "text"):
                    text = (result[0].text or "").strip()
                else:
                    continue
                
                if text:
                    return text
        except Exception:
            continue
    
    return None


def format_cnpj_cpf(doc: str) -> str:
    """
    Formata CNPJ ou CPF.
    
    Args:
        doc: Documento sem formatação
    
    Returns:
        Documento formatado
    """
    doc = doc.strip()
    
    if len(doc) == 14:  # CNPJ
        return f"{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:]}"
    elif len(doc) == 11:  # CPF
        return f"{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:]}"
    
    return doc


def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Trunca string adicionando reticências se necessário.
    
    Args:
        text: Texto a truncar
        max_length: Comprimento máximo
    
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def clean_xml_namespace(element: etree._Element) -> etree._Element:
    """
    Remove namespaces de um elemento XML (facilita XPath).
    
    Args:
        element: Elemento XML
    
    Returns:
        Elemento sem namespace
    """
    # Remove namespace de todas as tags
    for elem in element.iter():
        if isinstance(elem.tag, str):
            # Remove namespace prefix
            elem.tag = etree.QName(elem).localname
    
    # Remove atributos de namespace
    etree.cleanup_namespaces(element)
    
    return element


def is_valid_nfe_key(chave: str) -> bool:
    """
    Valida se chave de NF-e tem formato correto (44 dígitos).
    
    Args:
        chave: Chave da NF-e
    
    Returns:
        True se válida
    """
    if not chave:
        return False
    
    chave = chave.strip()
    return len(chave) == 44 and chave.isdigit()
