# Build do Executavel - Validador NF-e
# Script para gerar executavel Windows (.exe)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VALIDADOR NF-e - BUILD DO EXECUTAVEL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se esta no diretorio correto
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "Erro: Execute este script na raiz do projeto!" -ForegroundColor Red
    exit 1
}

# Verifica se o ambiente virtual existe
if (-not (Test-Path "venv")) {
    Write-Host "Ambiente virtual nao encontrado. Criando..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao criar ambiente virtual" -ForegroundColor Red
        exit 1
    }
}

# Ativa o ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
$env:Path = "$PWD\venv\Scripts;$env:Path"

# Instala/atualiza dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
& "$PWD\venv\Scripts\pip.exe" install --upgrade pip
& "$PWD\venv\Scripts\pip.exe" install -r requirements.txt
& "$PWD\venv\Scripts\pip.exe" install pyinstaller

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao instalar dependencias" -ForegroundColor Red
    exit 1
}

# Instala o pacote em modo desenvolvimento
Write-Host "Instalando pacote nfe_validator..." -ForegroundColor Yellow
& "$PWD\venv\Scripts\pip.exe" install -e .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao instalar pacote" -ForegroundColor Red
    exit 1
}

# Cria o icone se nao existir
if (-not (Test-Path "icon.ico")) {
    Write-Host "Icone nao encontrado. Criando icone..." -ForegroundColor Yellow
    
    # Tenta criar icone com Python
    $pythonCode = @'
try:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 236, 236], fill="#007bff", outline="#0056b3", width=8)
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    draw.text((80, 80), "NFe", fill="white", font=font)
    img.save("icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("OK")
except:
    print("ERRO")
'@
    
    $result = $pythonCode | & "$PWD\venv\Scripts\python.exe" 2>$null
    
    # Se falhar, cria icone vazio
    if (-not (Test-Path "icon.ico")) {
        Write-Host "Usando icone padrao..." -ForegroundColor Yellow
        New-Item -Path "icon.ico" -ItemType File -Force | Out-Null
    }
}

# Limpa builds anteriores
Write-Host "Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# Gera o executavel
Write-Host ""
Write-Host "Gerando executavel..." -ForegroundColor Cyan
Write-Host "Isso pode levar alguns minutos..." -ForegroundColor Yellow
Write-Host ""

& "$PWD\venv\Scripts\pyinstaller.exe" --clean ValidadorNFe.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Erro ao gerar executavel" -ForegroundColor Red
    exit 1
}

# Verifica se o executavel foi criado
if (Test-Path "dist\ValidadorNFe.exe") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  EXECUTAVEL GERADO COM SUCESSO!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Localizacao: dist\ValidadorNFe.exe" -ForegroundColor Cyan
    Write-Host ""
    
    # Mostra tamanho do arquivo
    $size = (Get-Item "dist\ValidadorNFe.exe").Length / 1MB
    Write-Host "Tamanho: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    
    # Pergunta se quer executar
    $response = Read-Host "Deseja executar o aplicativo agora? (S/N)"
    if ($response -eq "S" -or $response -eq "s") {
        Write-Host "Iniciando aplicativo..." -ForegroundColor Yellow
        Start-Process "dist\ValidadorNFe.exe"
    }
    
    Write-Host ""
    Write-Host "Dica: Voce pode copiar o arquivo ValidadorNFe.exe" -ForegroundColor Yellow
    Write-Host "para qualquer computador Windows e executa-lo" -ForegroundColor Yellow
    Write-Host "sem precisar instalar Python!" -ForegroundColor Yellow
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "Erro: Executavel nao foi gerado" -ForegroundColor Red
    Write-Host "Verifique os logs acima para detalhes" -ForegroundColor Yellow
    exit 1
}
