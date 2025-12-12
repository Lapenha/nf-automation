# Script de instalação automática
# Execute: .\install.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   Instalador - Validador NF-e IBS/CBS" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar versão do Python
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
    
    # Extrair versão numérica
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "❌ Python 3.11+ é necessário!" -ForegroundColor Red
            Write-Host "Baixe em: https://www.python.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
    }
} catch {
    Write-Host "❌ Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.11+ de: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Criar ambiente virtual
if (Test-Path "venv") {
    Write-Host "⚠️  Ambiente virtual já existe." -ForegroundColor Yellow
    $resposta = Read-Host "Deseja recriar? (S/N)"
    
    if ($resposta -eq "S" -or $resposta -eq "s") {
        Write-Host "🗑️  Removendo ambiente virtual antigo..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
    } else {
        Write-Host "✅ Usando ambiente virtual existente." -ForegroundColor Green
        & ".\venv\Scripts\Activate.ps1"
        Write-Host ""
        Write-Host "📦 Atualizando dependências..." -ForegroundColor Yellow
        pip install --upgrade pip
        pip install -r requirements.txt
        
        Write-Host ""
        Write-Host "✅ Instalação concluída!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📚 Próximos passos:" -ForegroundColor Cyan
        Write-Host "  1. Copie config.example.yaml para config.yaml" -ForegroundColor White
        Write-Host "  2. Edite config.yaml com suas preferências" -ForegroundColor White
        Write-Host "  3. Coloque XMLs na pasta 'xmls/'" -ForegroundColor White
        Write-Host "  4. Execute: python -m nfe_validator --config config.yaml" -ForegroundColor White
        Write-Host ""
        Write-Host "Ou use o script: .\run.ps1" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Pressione qualquer tecla para sair..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 0
    }
}

Write-Host "📦 Criando ambiente virtual..." -ForegroundColor Yellow
python -m venv venv

if (-Not (Test-Path "venv")) {
    Write-Host "❌ Falha ao criar ambiente virtual!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Ambiente virtual criado!" -ForegroundColor Green
Write-Host ""

# Ativar ambiente virtual
Write-Host "🔌 Ativando ambiente virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "✅ Ambiente ativado!" -ForegroundColor Green
Write-Host ""

# Atualizar pip
Write-Host "📦 Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""

# Instalar dependências
Write-Host "📦 Instalando dependências..." -ForegroundColor Yellow
Write-Host "   (Isso pode levar alguns minutos)" -ForegroundColor Gray
Write-Host ""

pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Erro ao instalar dependências!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente instalar manualmente:" -ForegroundColor Yellow
    Write-Host "  pip install lxml pandas openpyxl pyyaml tqdm python-dateutil" -ForegroundColor White
    Write-Host ""
    Write-Host "Se o erro for com 'lxml', tente:" -ForegroundColor Yellow
    Write-Host "  pip install --only-binary :all: lxml" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "✅ Todas as dependências instaladas!" -ForegroundColor Green
Write-Host ""

# Criar config.yaml se não existir
if (-Not (Test-Path "config.yaml")) {
    if (Test-Path "config.example.yaml") {
        Write-Host "📋 Criando config.yaml..." -ForegroundColor Yellow
        Copy-Item "config.example.yaml" "config.yaml"
        Write-Host "✅ config.yaml criado!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Próximos passos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Edite o arquivo de configuração:" -ForegroundColor White
Write-Host "   notepad config.yaml" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Coloque seus XMLs na pasta:" -ForegroundColor White
Write-Host "   xmls/" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Execute o validador:" -ForegroundColor White
Write-Host "   .\run.ps1" -ForegroundColor Gray
Write-Host "   OU" -ForegroundColor Yellow
Write-Host "   python -m nfe_validator --config config.yaml" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Documentação:" -ForegroundColor Cyan
Write-Host "   - README.md (completo)" -ForegroundColor Gray
Write-Host "   - QUICKSTART.md (guia rápido)" -ForegroundColor Gray
Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
