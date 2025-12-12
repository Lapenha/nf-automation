#!/bin/bash
# Build do Executável - Validador NF-e (Linux/WSL)
# Script para gerar executável

echo "========================================"
echo "  VALIDADOR NF-e - BUILD DO EXECUTÁVEL"
echo "========================================"
echo ""

# Verifica se está no diretório correto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto!"
    exit 1
fi

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual"
        exit 1
    fi
fi

# Ativa o ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala/atualiza dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Instala o pacote em modo desenvolvimento
echo "📦 Instalando pacote nfe_validator..."
pip install -e .

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar pacote"
    exit 1
fi

# Limpa builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf build dist

# Gera o executável
echo ""
echo "🚀 Gerando executável..."
echo "⏳ Isso pode levar alguns minutos..."
echo ""

pyinstaller --clean ValidadorNFe.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao gerar executável"
    exit 1
fi

# Verifica se o executável foi criado
if [ -f "dist/ValidadorNFe" ]; then
    echo ""
    echo "========================================"
    echo "  ✅ EXECUTÁVEL GERADO COM SUCESSO!"
    echo "========================================"
    echo ""
    echo "📍 Localização: dist/ValidadorNFe"
    echo ""
    
    # Mostra tamanho do arquivo
    size=$(du -h dist/ValidadorNFe | cut -f1)
    echo "📊 Tamanho: $size"
    echo ""
    
    # Torna executável
    chmod +x dist/ValidadorNFe
    
    echo "💡 Para executar: ./dist/ValidadorNFe"
    echo ""
    
else
    echo ""
    echo "❌ Erro: Executável não foi gerado"
    echo "Verifique os logs acima para detalhes"
    exit 1
fi
