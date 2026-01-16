# Validação de Tags XML Obrigatórias

## Nova Funcionalidade

Esta funcionalidade permite validar se os arquivos XML contêm todas as tags obrigatórias definidas na planilha de referência.

## Como Usar

1. **Abra o aplicativo** executando `python run_gui.py`

2. **Selecione os arquivos XML** usando:
   - **Arrastar e Soltar**: Arraste os arquivos XML diretamente para a área indicada
   - **Botão "Selecionar Pasta"**: Escolha uma pasta com múltiplos XMLs
   - **Botão "Adicionar Arquivo(s)"**: Selecione arquivos XML específicos

3. **Clique no botão "🏷️ VALIDAR TAGS XML OBRIGATÓRIAS"**

4. **Aguarde o processamento**:
   - O aplicativo carregará a planilha de referência
   - Validará cada XML contra as 180+ tags obrigatórias (1-1)
   - Mostrará o progresso em tempo real no log

5. **Visualize o relatório**:
   - Um arquivo Excel será gerado em `Downloads`
   - Nome: `relatorio_tags_obrigatorias_AAAAMMDD_HHMMSS.xlsx`
   - Contém:
     - **Aba "Resumo"**: Status geral de cada XML
     - **Aba "Tags Ausentes"**: Detalhes de cada tag ausente

## Planilha de Referência

A validação é baseada na planilha:
```
planilhabase/Mastersaf_Layout_DFe_V3_NFSe_NACIONAL_1_01 - Oficial Reforma.xlsx
```

**Aba utilizada**: "Emissão Nacional NFSe - V1.01"

**Critério de obrigatoriedade**: Tags com ocorrência "1-1" (uma e obrigatória)

## Estrutura do Relatório Excel

### Aba "Resumo"
| Coluna | Descrição |
|--------|-----------|
| Arquivo XML | Nome do arquivo validado |
| Status | ✅ OK ou ⚠️ Ausências |
| Tags Encontradas | Quantidade de tags presentes |
| Total Tags | Total de tags obrigatórias |
| Tags Ausentes | Quantidade de tags faltando |
| % Completude | Percentual de completude |

### Aba "Tags Ausentes"
| Coluna | Descrição |
|--------|-----------|
| Arquivo XML | Nome do arquivo |
| Nome da Tag | Nome do campo na planilha |
| Elemento | Tipo de elemento (E, G, CE, CG) |
| Tipo | Tipo de dado |
| Linha Planilha | Linha na planilha de referência |

## Interpretação dos Resultados

- **✅ Verde**: XML contém todas as tags obrigatórias
- **⚠️ Amarelo**: XML tem tags ausentes
- **% Completude**: 
  - 100% = Totalmente conforme
  - < 100% = Há tags ausentes

## Tipos de Elementos

- **E**: Elemento simples
- **G**: Grupo de elementos
- **CE**: Elemento condicional
- **CG**: Grupo condicional

## Observações Importantes

1. **Tags de Grupos**: Grupos marcadores (ex: `__DPS__`, `__prest__`) são ignorados na validação
2. **Namespace**: O validador remove namespaces do XML para simplificar a comparação
3. **Validação Estrutural**: Esta validação verifica apenas presença de tags, não valida valores ou formatos

## Diferença das Validações

### Validação IBS/CBS (Botão Verde)
- Valida cálculos de tributos IBS e CBS
- Compara valores calculados vs valores no XML
- Gera relatório de divergências de valores

### Validação de Tags (Botão Azul) 🆕
- Valida presença de tags obrigatórias
- Baseada na planilha oficial
- Gera relatório de tags ausentes

## Requisitos

- Python 3.8+
- Bibliotecas:
  - `openpyxl` (leitura/escrita Excel)
  - `lxml` (parse XML)
  - `PyQt6` (interface gráfica)

## Arquivos Relacionados

- `src/nfe_validator/tag_validator.py` - Módulo principal de validação
- `src/nfe_validator/gui.py` - Interface gráfica atualizada
- `tools/analyze_excel.py` - Ferramenta de análise da planilha

## Testando Via Linha de Comando

Você também pode testar diretamente:

```bash
python -m src.nfe_validator.tag_validator xmls/arquivo1.xml xmls/arquivo2.xml
```

Isso gerará um relatório em texto no console.
