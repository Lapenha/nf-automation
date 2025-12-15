; Inno Setup script para Validador NF-e
; Gera um instalador Windows que copia o EXE, o ícone e cria atalhos

[Setup]
AppName=Validador NF-e - IBS/CBS
AppVersion=1.0.0
AppId=com.lapenha.validadornfe
DefaultDirName={pf}\ValidadorNFe
DefaultGroupName=Validador NF-e
OutputBaseFilename=ValidadorNFe_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
DisableDirPage=no
DisableProgramGroupPage=no

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na &Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
; Executável principal e ícone
Source: "dist\ValidadorNFe.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.example.yaml"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Validador NF-e"; Filename: "{app}\ValidadorNFe.exe"; IconFilename: "{app}\icon.ico"
Name: "{userdesktop}\Validador NF-e"; Filename: "{app}\ValidadorNFe.exe"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\ValidadorNFe.exe"; Description: "Abrir Validador NF-e"; Flags: nowait postinstall skipifsilent
