<#
Script PowerShell para gerar o instalador com Inno Setup.
Ele procura pelo compilador ISCC (Inno Setup) e o executa com o arquivo `installer.iss`.

Uso:
  .\make_installer.ps1

Se o Inno Setup não estiver instalado, o script informará como instalar.
#>

Write-Host "== Gerar instalador (Inno Setup) ==" -ForegroundColor Cyan

$projectRoot = (Get-Item -Path .).FullName
$iss = Join-Path $projectRoot 'installer.iss'

if (-not (Test-Path $iss)) {
    Write-Host "Erro: não encontrei 'installer.iss' no diretório atual." -ForegroundColor Red
    exit 1
}

# Verifica se o executável empacotado existe
$exePath = Join-Path $projectRoot 'dist\ValidadorNFe.exe'
if (-not (Test-Path $exePath)) {
    Write-Host "Executável não encontrado: $exePath" -ForegroundColor Yellow
    Write-Host "Execute '.\build_exe.ps1' primeiro para gerar o EXE." -ForegroundColor Yellow
    exit 1
}

# Procura o compilador ISCC
$iscc = Get-Command iscc.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue
if (-not $iscc) {
    $candidates = @(
        "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe",
        "C:\\Program Files\\Inno Setup 6\\ISCC.exe"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { $iscc = $p; break }
    }
}

if (-not $iscc) {
    Write-Host "Não localizei o Inno Setup Compiler (ISCC)." -ForegroundColor Yellow
    Write-Host "Baixe e instale o Inno Setup: https://jrsoftware.org/isinfo.php" -ForegroundColor Cyan
    Write-Host "Depois rode este script novamente." -ForegroundColor Cyan
    exit 1
}

Write-Host "Usando ISCC: $iscc" -ForegroundColor Green
Write-Host "Compilando o instalador..." -ForegroundColor Cyan

& $iscc $iss
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao gerar o instalador (ISCC retornou código $LASTEXITCODE)." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Instalador gerado com sucesso (veja a saída do ISCC)." -ForegroundColor Green
