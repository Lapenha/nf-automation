# Estrutura do Projeto - NF-e IBS/CBS Validator

## 📁 Estrutura Completa

```
nf-automation/
│
├── 📄 README.md                      # Documentação completa
├── 📄 QUICKSTART.md                  # Guia rápido de uso
├── 📄 CHANGELOG.md                   # Histórico de versões
├── 📄 LICENSE                        # Licença MIT
├── 📄 .gitignore                     # Arquivos ignorados pelo Git
│
├── ⚙️ pyproject.toml                 # Configuração do projeto Python
├── 📦 requirements.txt               # Dependências do projeto
├── 🔧 config.example.yaml            # Exemplo de configuração
│
├── 🚀 install.ps1                    # Script de instalação (Windows)
├── 🚀 run.ps1                        # Script de execução (Windows)
│
├── 📂 src/
│   └── 📂 nfe_validator/             # Pacote principal
│       ├── __init__.py               # Inicialização do pacote
│       ├── __main__.py               # Entry point (python -m nfe_validator)
│       ├── cli.py                    # Interface CLI
│       ├── config.py                 # Sistema de configuração
│       ├── models.py                 # Modelos de dados (dataclasses)
│       ├── parser.py                 # Parser de XML NF-e
│       ├── calculator.py             # Cálculo de base IBS/CBS
│       ├── comparator.py             # Comparação com tolerância
│       ├── report.py                 # Gerador de relatório Excel
│       └── utils.py                  # Funções auxiliares
│
├── 📂 tests/                         # Testes unitários
│   ├── __init__.py
│   ├── test_parser_basic.py         # Testes do parser
│   ├── test_calculator.py           # Testes da calculadora
│   └── test_comparator.py           # Testes do comparador
│
├── 📂 xmls/                          # Pasta para XMLs de entrada
│   └── README.md                     # Instruções
│
└── 📂 output/                        # Pasta para relatórios
    └── README.md                     # Informações sobre saída
```

## 🎯 Arquivos Principais

### Core do Sistema

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| `models.py` | Dataclasses (NFe, Item, Result, etc.) | ~200 |
| `parser.py` | Parse de XML com lxml | ~300 |
| `calculator.py` | Cálculo de base IBS/CBS | ~150 |
| `comparator.py` | Comparação com tolerância | ~200 |
| `report.py` | Geração de Excel formatado | ~350 |
| `config.py` | Sistema de configuração YAML | ~250 |
| `utils.py` | Funções auxiliares | ~150 |
| `cli.py` | Interface de linha de comando | ~400 |

### Testes

| Arquivo | Descrição | Cenários |
|---------|-----------|----------|
| `test_parser_basic.py` | Testes de parsing | 2 cenários |
| `test_calculator.py` | Testes de cálculo | 5 cenários |
| `test_comparator.py` | Testes de comparação | 6 cenários |

## 📊 Métricas do Projeto

- **Linhas de código**: ~2.000+ linhas
- **Módulos**: 8 arquivos principais
- **Testes**: 13 testes unitários
- **Dependências**: 6 bibliotecas principais
- **Documentação**: 4 arquivos (README, QUICKSTART, etc.)

## 🔧 Tecnologias Utilizadas

### Principais
- **lxml** - Parse robusto de XML
- **pandas** - Manipulação de dados
- **openpyxl** - Geração e formatação de Excel
- **pyyaml** - Configuração YAML
- **tqdm** - Barra de progresso
- **decimal** - Precisão numérica

### Padrões
- Type hints (Python 3.11+)
- Dataclasses para modelos
- Arquitetura modular
- Separação de responsabilidades

## 🎨 Características do Design

### Modular
- Cada módulo tem responsabilidade única
- Fácil manutenção e extensão
- Testes independentes

### Configurável
- Arquivo YAML para configuração
- Múltiplos XPaths alternativos
- Componentes opcionais

### Robusto
- Tratamento completo de erros
- Logs detalhados
- Validações em múltiplas camadas

### Performático
- Processamento paralelo opcional
- Uso eficiente de memória
- Barra de progresso

## 📦 Fluxo de Dados

```
XMLs (entrada)
    ↓
Parser (lxml)
    ↓
Models (NFe, Item)
    ↓
Calculator (base IBS/CBS)
    ↓
Comparator (tolerância)
    ↓
ComparisonResult
    ↓
ReportGenerator (Excel)
    ↓
Relatório.xlsx (saída)
```

## 🚀 Processo de Execução

1. **Configuração**: Carrega config.yaml
2. **Descoberta**: Lista XMLs no input_dir
3. **Parse**: Extrai dados de cada XML
4. **Cálculo**: Calcula base IBS/CBS
5. **Comparação**: Compara com XML
6. **Agregação**: Consolida resultados
7. **Relatório**: Gera Excel formatado
8. **Log**: Salva log de execução

## 📈 Capacidade

- ✅ Processa **milhares** de XMLs
- ✅ Suporta **processamento paralelo**
- ✅ Gera relatórios **>100MB** sem problemas
- ✅ **<1 segundo** por XML (típico)
- ✅ Memória: **~100-500MB** (dependendo do volume)

## 🎓 Casos de Uso

1. **Auditoria Fiscal**: Validar cálculos de IBS/CBS
2. **Compliance**: Garantir conformidade com Reforma Tributária
3. **Análise em Massa**: Processar milhares de notas
4. **Debugging**: Identificar divergências específicas
5. **Relatórios**: Gerar evidências para auditorias

## 🔐 Segurança

- ✅ Processa localmente (offline)
- ✅ Não envia dados para servidores externos
- ✅ Logs configuráveis
- ✅ Sem hardcoded credentials

## 🌟 Destaques

- ✅ **100% Python** puro
- ✅ **Type hints** completos
- ✅ **Documentação** extensa
- ✅ **Testes** unitários
- ✅ **Configuração** flexível
- ✅ **CLI** intuitivo
- ✅ **Logs** detalhados
- ✅ **Excel** formatado profissionalmente

---

**Desenvolvido com ❤️ para facilitar a adequação à Reforma Tributária brasileira**
