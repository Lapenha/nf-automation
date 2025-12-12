"""
Script de teste rápido da GUI - Validador NF-e
"""

print("=" * 60)
print("  TESTE DA INTERFACE GRÁFICA - Validador NF-e")
print("=" * 60)
print()

# Testa imports
print("📦 Testando imports...")

try:
    from PyQt6.QtWidgets import QApplication
    print("   ✅ PyQt6.QtWidgets")
except ImportError as e:
    print(f"   ❌ PyQt6.QtWidgets: {e}")
    print("\n   Instale com: pip install PyQt6")
    exit(1)

try:
    from PyQt6.QtCore import Qt, QThread
    print("   ✅ PyQt6.QtCore")
except ImportError as e:
    print(f"   ❌ PyQt6.QtCore: {e}")
    exit(1)

try:
    from PyQt6.QtGui import QFont
    print("   ✅ PyQt6.QtGui")
except ImportError as e:
    print(f"   ❌ PyQt6.QtGui: {e}")
    exit(1)

try:
    from nfe_validator.gui import MainWindow, DropArea, ValidationThread
    print("   ✅ nfe_validator.gui")
except ImportError as e:
    print(f"   ❌ nfe_validator.gui: {e}")
    print("\n   Execute: pip install -e .")
    exit(1)

try:
    from nfe_validator.cli import NFeValidator
    print("   ✅ nfe_validator.cli")
except ImportError as e:
    print(f"   ❌ nfe_validator.cli: {e}")
    exit(1)

try:
    from nfe_validator.config import load_config
    print("   ✅ nfe_validator.config")
except ImportError as e:
    print(f"   ❌ nfe_validator.config: {e}")
    exit(1)

print("\n✅ Todos os imports OK!")
print()

# Testa criação da aplicação
print("🎨 Testando criação da aplicação...")

try:
    import sys
    app = QApplication(sys.argv)
    print("   ✅ QApplication criada")
    
    window = MainWindow()
    print("   ✅ MainWindow criada")
    
    # Não mostra a janela, apenas testa a criação
    print("\n✅ Interface gráfica funcionando corretamente!")
    print()
    print("💡 Para executar a GUI, use:")
    print("   python -m nfe_validator.gui")
    print()
    print("🚀 Para gerar o executável, use:")
    print("   .\\build_exe.ps1")
    print()
    
except Exception as e:
    print(f"\n❌ Erro ao criar interface: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("=" * 60)
