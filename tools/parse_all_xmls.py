#!/usr/bin/env python3
"""Script auxiliar: parseia todos os arquivos em ./xmls usando NFeParser
Imprime contagem de itens e tags por item para validar extração de tags por `det[nItem]`.
"""
from pathlib import Path
import sys
import traceback

repo = Path(__file__).resolve().parents[1]
src = repo / 'src'
sys.path.insert(0, str(src))

from nfe_validator.parser import NFeParser
from nfe_validator.config import load_config, Config


def main():
    # carregar configuração (usar config.yaml ou config.example.yaml se existir)
    cfg = load_config() if (Path('config.yaml').exists() or Path('config.example.yaml').exists()) else Config()
    parser = NFeParser(cfg)

    xml_dir = repo / 'xmls'
    if not xml_dir.exists():
        print('Diretório xmls/ não encontrado')
        return

    files = sorted([p for p in xml_dir.iterdir() if p.is_file() and p.suffix.lower() in ('.xml', '.txt')])
    if not files:
        print('Nenhum arquivo .xml ou .txt encontrado em xmls/')
        return

    for p in files:
        print('---', p.name, '---')
        try:
            nfe = parser.parse_file(p)
            if nfe is None:
                print('  parse retornou None')
                continue

            print(f"  chave: {nfe.chave!r}, itens: {len(nfe.itens)}, tags total: {len(nfe.tags)}")

            for item in nfe.itens:
                # coletar chaves de tags que correspondem ao item (det[nItem])
                keys = [k for k in nfe.tags.keys() if f"det[{item.nItem}]" in k]
                print(f"   - item {item.nItem}: keys {len(keys)}, ibs_found={item.ibs_xml.found}, cbs_found={item.cbs_xml.found}")
                for k in keys[:6]:
                    print(f"      {k} => {nfe.tags[k]!r}")
                if len(keys) > 6:
                    print(f"      ... +{len(keys)-6} more")

        except Exception:
            print('  Exception ao processar arquivo:')
            traceback.print_exc()


if __name__ == '__main__':
    main()
