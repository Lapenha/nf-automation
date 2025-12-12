# -*- mode: python ; coding: utf-8 -*-
"""
Spec file para PyInstaller - Validador NF-e GUI
Gera executável standalone para Windows
"""

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.example.yaml', '.'),
    ],
    hiddenimports=[
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'pandas',
        'openpyxl',
        'PyQt6.sip',
        'nfe_validator',
        'nfe_validator.cli',
        'nfe_validator.config',
        'nfe_validator.models',
        'nfe_validator.parser',
        'nfe_validator.calculator',
        'nfe_validator.comparator',
        'nfe_validator.report',
        'nfe_validator.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ValidadorNFe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem janela de console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Sem icone por enquanto
)
