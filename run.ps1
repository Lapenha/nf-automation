# Script de execução do validador NF-e IBS/CBS
# Execute: .\run.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   Validador NF-e IBS/CBS - Reforma Tributária" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o ambiente virtual existe
if (-Not (Test-Path "venv")) {
    Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: python -m venv venv" -ForegroundColor Yellow
    Write-Host "Depois: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "E então: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Verificar se o ambiente virtual está ativado
if (-Not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Ativando ambiente virtual..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Verificar se config.yaml existe
if (-Not (Test-Path "config.yaml")) {
    Write-Host "⚠️  Arquivo config.yaml não encontrado!" -ForegroundColor Yellow
    
    if (Test-Path "config.example.yaml") {
        Write-Host "📋 Criando config.yaml a partir do exemplo..." -ForegroundColor Cyan
        Copy-Item "config.example.yaml" "config.yaml"
        Write-Host "✅ config.yaml criado! Edite conforme necessário." -ForegroundColor Green
        Write-Host ""
        
        $resposta = Read-Host "Deseja editar o arquivo agora? (S/N)"
        if ($resposta -eq "S" -or $resposta -eq "s") {
            notepad config.yaml
            Write-Host "Pressione qualquer tecla após editar o arquivo..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    } else {
        Write-Host "❌ config.example.yaml também não encontrado!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🚀 Iniciando validação..." -ForegroundColor Green
Write-Host ""

# Executar o validador
python -m nfe_validator --config config.yaml

# Verificar resultado
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Validação concluída com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Verifique os relatórios na pasta 'output/'" -ForegroundColor Cyan
    
    # Abrir pasta output
    if (Test-Path "output") {
        $resposta = Read-Host "Deseja abrir a pasta de relatórios? (S/N)"
        if ($resposta -eq "S" -or $resposta -eq "s") {
            Invoke-Item "output"
        }
    }
} else {
    Write-Host ""
    Write-Host "❌ Erro durante a validação!" -ForegroundColor Red
    Write-Host "Verifique os logs na pasta 'output/' para mais detalhes." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
