# Guia Rápido de Uso

## 1. Instalação Rápida

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

## 2. Configuração Inicial

```powershell
# Copiar arquivo de configuração de exemplo
Copy-Item config.example.yaml config.yaml

# Editar config.yaml com suas preferências
notepad config.yaml
```

Ajuste pelo menos:
- `input_dir`: pasta com seus XMLs
- `output_dir`: onde salvar relatórios
- `workers`: número de processadores (recomendo 4-8)

## 3. Preparar XMLs

Organize seus XMLs de NF-e:
```
xmls/
├── 2025-01/
│   ├── nfe_001.xml
│   ├── nfe_002.xml
│   └── ...
└── 2025-02/
    ├── nfe_003.xml
    └── ...
```

## 4. Executar Validação

### Modo padrão (usando config.yaml)
```powershell
python -m nfe_validator --config config.yaml
```

### Teste rápido (primeiros 10 arquivos)
```powershell
python -m nfe_validator --input ./xmls --output ./output --max-files 10
```

### Processamento paralelo (4 threads)
```powershell
python -m nfe_validator --config config.yaml --workers 4
```

## 5. Verificar Resultados

Os relatórios estarão em `output/`:
- `relatorio_ibs_cbs_YYYYMMDD_HHMMSS.xlsx` - Relatório Excel
- `validador_YYYYMMDD_HHMMSS.log` - Log detalhado

## 6. Análise do Relatório Excel

### Aba "Resumo NF"
- Veja o status de cada nota: OK, DIVERGENTE ou SEM_TAG
- Verde = OK, Vermelho = Divergente, Amarelo = Sem tags IBS/CBS

### Aba "Divergências"
- Foco nos problemas identificados
- Use filtros para analisar por produto, fornecedor, etc.

### Aba "Erros"
- XMLs que não puderam ser processados
- Verifique a mensagem de erro para corrigir

## 7. Ajustes Comuns

### Tolerância muito rígida? Ajuste:
```yaml
tolerance:
  absolute: 0.10  # Era 0.05
  percentage: 0.2  # Era 0.1
```

### Adicionar IPI na base?
```yaml
include_components:
  ipi: true  # Era false
```

### XMLs com estrutura diferente?
Ajuste os XPaths em `config.yaml`:
```yaml
xpaths:
  ibs:
    base_paths:
      - ".//*[local-name()='MEU_TAG_IBS']/*[local-name()='vBC']"
```

## 8. Dicas de Performance

- Use `--workers 4` ou mais para processar milhares de XMLs
- Teste primeiro com `--max-files 100` antes de processar tudo
- Use `--debug` apenas para investigar problemas específicos

## 9. Solução Rápida de Problemas

**Erro ao instalar lxml?**
```powershell
pip install --upgrade pip
pip install lxml --only-binary :all:
```

**Permissão negada no PowerShell?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Excel não abre?**
- Verifique se tem o Microsoft Excel instalado ou use LibreOffice
- Formato XLSX é padrão e compatível

## 10. Próximos Passos

- Automatize com Task Scheduler (Windows) ou cron (Linux)
- Integre com seu sistema ERP/fiscal
- Personalize os XPaths para seu layout de XML

---

**Suporte:** Abra uma issue no GitHub para dúvidas ou problemas.
