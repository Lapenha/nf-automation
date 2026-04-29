# 🧾 Validador de NF-e IBS/CBS

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Validação em massa de XMLs de NF-e (modelo 55) com foco em IBS/CBS da Reforma Tributária.**

Sistema profissional para validar cálculos de IBS (Imposto sobre Bens e Serviços) e CBS (Contribuição sobre Bens e Serviços) em Notas Fiscais Eletrônicas, comparando valores calculados conforme fórmula configurável com valores informados no XML.

---

##  Funcionalidades

- ✅ **Processamento em massa** de XMLs de NF-e (centenas/milhares de arquivos)
- ✅ **Cálculo automático** da base de IBS/CBS por item com fórmula configurável
- ✅ **Comparação inteligente** com tolerância absoluta e percentual
- ✅ **Extração robusta** de dados usando XPath configurável (ignora namespace)
- ✅ **Relatório Excel** completo com 4 abas:
  - **Resumo NF**: Visão consolidada por nota fiscal
  - **Itens**: Detalhamento item a item
  - **Divergências**: Apenas registros com problemas (filtrado)
  - **Erros**: XMLs que falharam no processamento
- ✅ **Formatação profissional** no Excel (cores, filtros, freeze panes, auto-width)
- ✅ **Processamento paralelo** opcional para máxima performance
- ✅ **Logs detalhados** para auditoria e debug
- ✅ **Configuração flexível** via arquivo YAML ou argumentos CLI

---

##  Requisitos

- **Python 3.11+**
- Sistema operacional: Windows, Linux ou macOS

---

##  Instalação

### 1. Clone ou baixe o projeto

```powershell
cd c:\Users\MuriloAlapenhaSoares\nf-automation
```

### 2. Crie um ambiente virtual

```powershell
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```powershell
pip install -r requirements.txt
```

Ou para instalação completa (modo desenvolvimento):

```powershell
pip install -e .
```

---

##  Interface Gráfica (Nova!)

**Agora com interface visual moderna e intuitiva!**

### Como Usar a GUI

#### Opção 1: Executável Standalone (Recomendado)

```powershell
# Gerar o executável
.\build_exe.ps1

# O executável estará em: dist\ValidadorNFe.exe
# Pode ser copiado para qualquer computador Windows!
```

#### Opção 2: Executar com Python

```powershell
# Após instalação
python -m nfe_validator.gui
```

### Recursos da Interface

-  **Arrastar e Soltar**: Arraste XMLs diretamente para a janela
-  **Seleção de Pasta**: Escolha uma pasta com múltiplos XMLs
-  **Múltiplos Arquivos**: Adicione arquivos individualmente
-  **Progresso em Tempo Real**: Barra de progresso e logs visuais
-  **Salva em Downloads**: Relatório automaticamente salvo na pasta Downloads
-  **Design Moderno**: Interface limpa e profissional

> **Veja o [GUI_GUIDE.md](GUI_GUIDE.md) para guia completo com screenshots!**

---

## ⚙️ Configuração

### 1. Copie o arquivo de exemplo

```powershell
Copy-Item config.example.yaml config.yaml
```

### 2. Edite `config.yaml` conforme sua necessidade

```yaml
# Diretórios
input_dir: "./xmls"              # Pasta com os XMLs
output_dir: "./output"           # Pasta para relatórios

# Tolerâncias
tolerance:
  absolute: 0.05                 # R$ 0,05
  percentage: 0.1                # 0,1%

# Componentes da fórmula de cálculo
include_components:
  freight: true                  # Incluir frete
  insurance: true                # Incluir seguro
  other: true                    # Incluir outras despesas
  discount: true                 # Subtrair desconto
  ipi: false                     # Incluir IPI
  # ... outros componentes

# Execução
execution:
  workers: 4                     # Processamento paralelo (4 threads)
  recurse_subfolders: true       # Buscar em subpastas
  debug: false                   # Modo debug
```

### Fórmula de Cálculo da Base

Por padrão (configurável):

```
Base = vProd + vFrete + vSeg + vOutro - vDesc
```

Você pode habilitar componentes adicionais (IPI, II, ICMS-ST, etc.) editando o arquivo de configuração.

---

## 📖 Uso

### Modo básico (usando arquivo de configuração)

```powershell
python -m nfe_validator --config config.yaml
```

---

## 🛠️ Gerar Instalador Windows (Inno Setup)

Se você quer distribuir o programa para outros computadores Windows com um instalador profissional (cria atalho no menu Iniciar e na Área de Trabalho), use o Inno Setup.

1) Gere o executável primeiro (já feito pelo script de build):

```powershell
.\venv\Scripts\Activate.ps1
.\build_exe.ps1
```

2) Gere o instalador com Inno Setup:

- Instale o Inno Setup: https://jrsoftware.org/isinfo.php
- Depois execute no diretório do projeto:

```powershell
.\make_installer.ps1
```

O script procura por `iscc.exe` (Inno Setup Compiler) e compilá `installer.iss`, produzindo um instalador `.exe`.

O instalador inclui o `dist\ValidadorNFe.exe`, `icon.ico` e `config.example.yaml`, e cria atalhos no Menu Iniciar e (opcional) na Área de Trabalho.


### Sobrescrever configurações via CLI

```powershell
python -m nfe_validator --input ./meus_xmls --output ./relatorios --workers 4
```

### Exemplos avançados

**Processar com tolerâncias customizadas:**
```powershell
python -m nfe_validator --config config.yaml --tol-abs 0.10 --tol-pct 0.2
```

**Processar apenas 100 arquivos (teste):**
```powershell
python -m nfe_validator --input ./xmls --max-files 100
```

**Modo debug:**
```powershell
python -m nfe_validator --config config.yaml --debug
```

**Não buscar em subpastas:**
```powershell
python -m nfe_validator --input ./xmls --no-recurse
```

### Argumentos disponíveis

| Argumento | Descrição |
|-----------|-----------|
| `--config` | Arquivo YAML de configuração |
| `--input` | Diretório de entrada (XMLs) |
| `--output` | Diretório de saída (relatórios) |
| `--tol-abs` | Tolerância absoluta (R$) |
| `--tol-pct` | Tolerância percentual (%) |
| `--workers` | Número de threads paralelos |
| `--max-files` | Limite de arquivos |
| `--debug` | Ativa modo debug |
| `--no-recurse` | Não buscar em subpastas |

---

## Estrutura do Relatório Excel

### Aba "Resumo NF"
Visão consolidada de cada nota fiscal:
- Chave de acesso, número, série, data
- Emitente e destinatário
- Totalizadores de base e valores IBS/CBS
- Contagem de divergências por nota
- **Status geral** (OK / DIVERGENTE / SEM_TAG)

### Aba "Itens"
Detalhamento item a item:
- Código e descrição do produto
- Base calculada vs. base informada (IBS e CBS)
- Alíquotas e valores informados
- Deltas (diferenças) calculados
- Flags de divergência

### Aba "Divergências"
Apenas itens com problemas identificados (facilita auditoria).

### Aba "Erros"
XMLs que falharam no processamento com descrição do erro.

### Aba "Configuração"
Resumo da configuração usada no processamento (fórmula, tolerâncias, etc.).

---

## Testes

Execute os testes unitários:

```powershell
python -m pytest tests/
```

Ou individualmente:

```powershell
python -m pytest tests/test_parser_basic.py
python -m pytest tests/test_calculator.py
python -m pytest tests/test_comparator.py
```

---

## Estrutura do Projeto

```
nf-automation/
├── src/
│   └── nfe_validator/
│       ├── __init__.py          # Exportações principais
│       ├── __main__.py          # Entry point (python -m nfe_validator)
│       ├── cli.py               # Interface CLI
│       ├── config.py            # Sistema de configuração
│       ├── models.py            # Modelos de dados (dataclasses)
│       ├── parser.py            # Parser de XML NF-e
│       ├── calculator.py        # Cálculo de base IBS/CBS
│       ├── comparator.py        # Comparação com tolerância
│       ├── report.py            # Gerador de Excel
│       └── utils.py             # Funções auxiliares
├── tests/
│   ├── __init__.py
│   ├── test_parser_basic.py    # Testes do parser
│   ├── test_calculator.py      # Testes da calculadora
│   └── test_comparator.py      # Testes do comparador
├── config.example.yaml          # Exemplo de configuração
├── pyproject.toml               # Configuração do projeto
├── requirements.txt             # Dependências
└── README.md                    # Este arquivo
```

---

## 🔧 Tecnologias Utilizadas

- **lxml**: Parse robusto de XML com suporte a XPath
- **pandas**: Manipulação de dados tabulares
- **openpyxl**: Geração e formatação de Excel
- **pyyaml**: Leitura de configurações YAML
- **tqdm**: Barra de progresso no console
- **decimal**: Precisão numérica para valores monetários

---

## Regras de Negócio

### Tolerâncias

O sistema usa **duas tolerâncias** e aplica a **mais permissiva**:

1. **Tolerância absoluta**: Diferença máxima em reais (ex: R$ 0,05)
2. **Tolerância percentual**: Diferença máxima em % do valor de referência (ex: 0,1%)

**Critério de divergência:**
```
|valor_calculado - valor_informado| > max(tol_abs, tol_pct * |valor_informado|)
```

### Status

- **OK**: Todos os valores dentro da tolerância
- **DIVERGENTE**: Pelo menos um valor fora da tolerância
- **SEM_TAG**: Tags IBS/CBS não encontradas no XML (não é erro, apenas informativo)

### XPaths Flexíveis

O parser busca tags IBS/CBS usando `local-name()` para **ignorar namespaces**, e tenta múltiplos XPaths configuráveis. Isso garante compatibilidade com diferentes layouts de XML.

---

## Solução de Problemas

### Erro: "Nenhum arquivo XML encontrado"
- Verifique se o caminho do `input_dir` está correto
- Verifique se os arquivos têm extensão `.xml`

### Erro: "Falha ao fazer parse do XML"
- Valide se o XML está bem formado
- Verifique a aba "Erros" no relatório para detalhes

### Divergências inesperadas
- Ajuste as tolerâncias no arquivo de configuração
- Verifique se a fórmula de cálculo está correta (componentes habilitados/desabilitados)
- Use `--debug` para ver logs detalhados

### Performance lenta
- Aumente o número de `workers` para processamento paralelo
- Exemplo: `--workers 8` para 8 threads

---

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## Autor

**Murilo Alapenha Soares**

- GitHub: [@muriloalapenhaSoares](https://github.com/muriloalapenhaSoares)

---

## Agradecimentos

- Projeto desenvolvido para auxiliar na adequação à Reforma Tributária brasileira
- Foco em automação e conformidade fiscal

---

## Suporte

Para dúvidas ou problemas, abra uma [issue](https://github.com/muriloalapenhaSoares/nfe-ibs-cbs-validator/issues) no GitHub.

---

** Validação fiscal eficiente e confiável com Python!**
