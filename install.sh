#!/bin/bash
# Script de instalação para Linux/WSL

echo "==============================================="
echo "   Instalador - Validador NF-e IBS/CBS (WSL)"
echo "==============================================="
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instale com: sudo apt update && sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION encontrado"
echo ""

# Criar ambiente virtual
if [ -d "venv" ]; then
    echo "⚠️  Ambiente virtual já existe."
    read -p "Deseja recriar? (s/N): " resposta
    if [[ "$resposta" =~ ^[Ss]$ ]]; then
        echo "🗑️  Removendo ambiente virtual antigo..."
        rm -rf venv
    else
        echo "✅ Usando ambiente virtual existente."
        source venv/bin/activate
        echo ""
        echo "📦 Atualizando dependências..."
        pip install --upgrade pip
        pip install -r requirements.txt
        
        echo ""
        echo "✅ Instalação concluída!"
        echo ""
        echo "📚 Próximos passos:"
        echo "  1. cp config.example.yaml config.yaml"
        echo "  2. nano config.yaml  # Edite conforme necessário"
        echo "  3. Coloque XMLs na pasta 'xmls/'"
        echo "  4. python3 -m nfe_validator --config config.yaml"
        echo ""
        exit 0
    fi
fi

echo "📦 Criando ambiente virtual..."
python3 -m venv venv

if [ ! -d "venv" ]; then
    echo "❌ Falha ao criar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual criado!"
echo ""

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

echo "✅ Ambiente ativado!"
echo ""

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
echo "   (Isso pode levar alguns minutos)"
echo ""

pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao instalar dependências!"
    echo ""
    echo "Tente instalar manualmente:"
    echo "  pip install lxml pandas openpyxl pyyaml tqdm python-dateutil"
    echo ""
    exit 1
fi

echo ""
echo "✅ Todas as dependências instaladas!"
echo ""

# Criar config.yaml se não existir
if [ ! -f "config.yaml" ] && [ -f "config.example.yaml" ]; then
    echo "📋 Criando config.yaml..."
    cp config.example.yaml config.yaml
    echo "✅ config.yaml criado!"
fi

echo ""
echo "==============================================="
echo "   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "==============================================="
echo ""
echo "📚 Próximos passos:"
echo ""
echo "1. Edite o arquivo de configuração:"
echo "   nano config.yaml"
echo ""
echo "2. Coloque seus XMLs na pasta:"
echo "   xmls/"
echo ""
echo "3. Execute o validador:"
echo "   source venv/bin/activate"
echo "   python3 -m nfe_validator --config config.yaml"
echo ""
echo "📖 Documentação:"
echo "   - README.md (completo)"
echo "   - QUICKSTART.md (guia rápido)"
echo ""
-