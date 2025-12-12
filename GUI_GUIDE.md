# Guia de Uso - Interface Gráfica

## 🎨 Interface do Usuário

O Validador NF-e agora possui uma **interface gráfica moderna e intuitiva**!

### 📥 Como Usar

#### 1. **Adicionar Arquivos XML**

Você tem 3 formas de adicionar arquivos:

- **🖱️ Arrastar e Soltar**: Arraste arquivos XML diretamente para a área central
- **📂 Selecionar Pasta**: Clique em "Selecionar Pasta" e escolha uma pasta com XMLs
- **📄 Adicionar Arquivos**: Clique em "Adicionar Arquivo(s)" para selecionar XMLs individuais

#### 2. **Processar**

- Clique no botão verde **"▶️ INICIAR VALIDAÇÃO"**
- Acompanhe o progresso em tempo real na barra de progresso
- Veja os logs detalhados na área de texto

#### 3. **Resultado**

- Quando concluído, você verá um resumo completo da validação
- O relatório Excel será salvo automaticamente na pasta **Downloads**
- Você pode:
  - **Abrir o Relatório** diretamente
  - **Abrir a Pasta** Downloads
  - **Fechar** e processar mais arquivos

### ✨ Recursos

- ✅ **Drag & Drop**: Interface moderna com arrastar e soltar
- ✅ **Múltiplos Arquivos**: Processe vários XMLs de uma vez
- ✅ **Progresso Visual**: Barra de progresso e logs em tempo real
- ✅ **Salva Automaticamente**: Relatório vai direto para Downloads
- ✅ **Design Limpo**: Interface profissional e fácil de usar

---

## 🚀 Como Executar

### Opção 1: Instalar e Executar (Desenvolvimento)

```powershell
# Instalar dependências
.\install.ps1

# Executar GUI
python -m nfe_validator.gui
```

Ou no WSL/Linux:

```bash
# Instalar dependências
./install.sh

# Executar GUI
python3 -m nfe_validator.gui
```

### Opção 2: Executável Standalone (Recomendado)

#### Windows

1. **Criar o Ícone** (opcional, mas recomendado):
```powershell
pip install Pillow
python create_icon.py
```

2. **Gerar o Executável**:
```powershell
.\build_exe.ps1
```

3. **Executar**:
   - O executável estará em: `dist\ValidadorNFe.exe`
   - Pode ser copiado para qualquer computador Windows
   - **Não precisa instalar Python!** 🎉

#### Linux/WSL

```bash
chmod +x build_exe.sh
./build_exe.sh
./dist/ValidadorNFe
```

---

## 📦 Distribuição

### Para Usuários Finais

O executável `ValidadorNFe.exe` pode ser distribuído diretamente:

1. ✅ **Sem instalação**: Basta copiar o arquivo .exe
2. ✅ **Sem Python**: Funciona em qualquer Windows 10/11
3. ✅ **Standalone**: Todas as dependências incluídas
4. ✅ **Sem configuração**: Usa configurações padrão

### Tamanho do Executável

- **Esperado**: ~50-80 MB (comprimido com UPX)
- Inclui: Python, PyQt6, lxml, pandas, openpyxl e todas as dependências

---

## 🎯 Interface Visual

### Tela Principal

```
┌─────────────────────────────────────────────┐
│     🧾 Validador de NF-e - IBS/CBS         │
│  Validação automática de tributos da RT    │
├─────────────────────────────────────────────┤
│                                              │
│            ┌──────────────────┐             │
│            │       📁         │             │
│            │                  │             │
│            │  Arraste XMLs    │             │
│            │  aqui ou clique  │             │
│            │  em Selecionar   │             │
│            │                  │             │
│            └──────────────────┘             │
│                                              │
│  [📂 Pasta]  [📄 Arquivos]  [🗑️ Limpar]   │
│                                              │
│         5 arquivos selecionados              │
│                                              │
│        [▶️ INICIAR VALIDAÇÃO]               │
│                                              │
│  ████████████████░░░░ 80% (4/5 arquivos)   │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │ 🚀 Iniciando validação...          │    │
│  │ 📁 5 arquivo(s) XML encontrado(s)  │    │
│  │ ⚙️  Processando: teste_001.xml     │    │
│  │    ✅ OK                            │    │
│  │ ...                                 │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Solução de Problemas

### Erro ao Gerar Executável

**Problema**: PyInstaller não está instalado
```powershell
pip install pyinstaller
```

**Problema**: Módulo não encontrado durante build
- Certifique-se de que o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### Erro ao Executar GUI

**Problema**: PyQt6 não está instalado
```powershell
pip install PyQt6
```

**Problema**: "No module named nfe_validator"
```powershell
pip install -e .
```

### Ícone Não Aparece

Se o ícone não for criado automaticamente:
```powershell
pip install Pillow
python create_icon.py
```

---

## 📝 Notas Técnicas

### Tecnologias Usadas

- **PyQt6**: Framework para interface gráfica moderna
- **QThread**: Processamento em background (não trava a interface)
- **Drag & Drop**: Suporte nativo para arrastar arquivos
- **PyInstaller**: Empacotamento em executável standalone

### Configuração

A GUI usa as mesmas configurações do CLI:
- Arquivo: `config.yaml` (ou `config.example.yaml`)
- Tolerâncias configuráveis
- Componentes de cálculo configuráveis
- XPaths customizáveis

### Logs

Os logs são exibidos em tempo real na interface e também salvos em:
- `output/validador_YYYYMMDD_HHMMSS.log`

---

## 🎉 Pronto!

Agora sua mãe pode usar o validador com uma interface bonita e fácil! 

**Características para usuários não técnicos:**
- ✅ Interface visual clara
- ✅ Arrastar e soltar arquivos
- ✅ Botões grandes e descritivos
- ✅ Progresso visual em tempo real
- ✅ Salva automaticamente em Downloads
- ✅ Mensagens de sucesso/erro claras
- ✅ Opção de abrir o relatório automaticamente

**Não precisa saber:**
- ❌ Linha de comando
- ❌ Python
- ❌ Configurações técnicas
- ❌ Onde ficam os arquivos
