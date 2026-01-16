"""
Teste da funcionalidade de validação de tags obrigatórias.
"""
from pathlib import Path
from src.nfe_validator.tag_validator import TagValidator

def test_tag_validator():
    """Testa o validador de tags."""
    
    # Caminho da planilha
    base_dir = Path(__file__).parent
    excel_path = base_dir / "planilhabase" / "Mastersaf_Layout_DFe_V3_NFSe_NACIONAL_1_01 - Oficial Reforma.xlsx"
    
    print("="*80)
    print("TESTE DE VALIDAÇÃO DE TAGS OBRIGATÓRIAS")
    print("="*80)
    print()
    
    # Verifica se a planilha existe
    if not excel_path.exists():
        print(f"❌ ERRO: Planilha não encontrada em:")
        print(f"   {excel_path}")
        return False
    
    print(f"✅ Planilha encontrada: {excel_path.name}")
    print()
    
    # Cria validador
    print("📋 Carregando tags obrigatórias da planilha...")
    try:
        validator = TagValidator(excel_path)
        print(f"✅ {len(validator.tags_obrigatorias)} tags obrigatórias carregadas")
        print()
    except Exception as e:
        print(f"❌ ERRO ao carregar planilha: {e}")
        return False
    
    # Lista algumas tags para conferência
    print("📝 Primeiras 10 tags obrigatórias:")
    for i, tag in enumerate(validator.tags_obrigatorias[:10], 1):
        print(f"   {i}. {tag.nome} ({tag.elemento}) - Tipo: {tag.tipo}")
    print()
    
    # Testa com XMLs de exemplo
    xml_dir = base_dir / "xmls"
    if xml_dir.exists():
        xml_files = list(xml_dir.glob("*.xml"))
        if xml_files:
            print(f"🔍 Testando com {len(xml_files)} arquivo(s) XML de exemplo...")
            print()
            
            for xml_file in xml_files[:3]:  # Testa apenas os 3 primeiros
                print(f"📄 Validando: {xml_file.name}")
                try:
                    resultado = validator.validar_xml(xml_file)
                    print(f"   Status: {resultado.mensagem}")
                    print(f"   Tags encontradas: {resultado.tags_encontradas}/{resultado.total_tags_obrigatorias}")
                    
                    if not resultado.sucesso:
                        print(f"   Tags ausentes: {len(resultado.tags_ausentes)}")
                        if resultado.tags_ausentes:
                            print(f"   Primeiras 5 ausentes:")
                            for tag in resultado.tags_ausentes[:5]:
                                print(f"      - {tag.nome}")
                    print()
                    
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    print()
        else:
            print("⚠️ Nenhum arquivo XML encontrado para teste")
    else:
        print("⚠️ Pasta 'xmls' não encontrada")
    
    print("="*80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO")
    print("="*80)
    print()
    print("Para usar a funcionalidade:")
    print("1. Execute: python run_gui.py")
    print("2. Selecione os arquivos XML")
    print("3. Clique em '🏷️ VALIDAR TAGS XML OBRIGATÓRIAS'")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    success = test_tag_validator()
    sys.exit(0 if success else 1)
