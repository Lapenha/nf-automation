#!/usr/bin/env python3
"""Script para testar se os itens têm cProd acessível."""
from pathlib import Path
import sys

repo = Path(__file__).resolve().parents[1]
src = repo / 'src'
sys.path.insert(0, str(src))

from nfe_validator.parser import NFeParser
from nfe_validator.config import Config

cfg = Config()
parser = NFeParser(cfg)

xml_path = repo / 'xmls' / 'test_nfe_10_items.xml'
nfe = parser.parse_file(xml_path)

if nfe:
    print(f"NFe tem {len(nfe.itens)} itens")
    for item in nfe.itens[:3]:
        print(f"  Item {item.nItem}: cProd={item.cProd!r}")
    
    print(f"\nNFe tem {len(nfe.tags)} tags")
    # mostrar algumas tags de det[1]
    det1_tags = {k: v for k, v in nfe.tags.items() if 'det[1]' in k}
    print(f"Tags de det[1]: {len(det1_tags)}")
    for k in list(det1_tags.keys())[:3]:
        print(f"  {k} => {det1_tags[k]!r}")
