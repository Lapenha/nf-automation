"""
Ponto de entrada para o executavel GUI do Validador NF-e.
Este arquivo nao usa imports relativos para compatibilidade com PyInstaller.
"""
import sys
import os

# Adiciona o diretorio src ao path para permitir imports absolutos
if getattr(sys, 'frozen', False):
    # Executando como executavel PyInstaller
    application_path = sys._MEIPASS
else:
    # Executando como script Python
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(application_path, 'src'))

# Agora importa e executa a GUI
from nfe_validator.gui import main

if __name__ == "__main__":
    main()
