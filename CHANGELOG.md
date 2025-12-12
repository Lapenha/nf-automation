# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-12-12

### 🎉 Primeira Versão

#### Adicionado
- ✅ Parser robusto de XML NF-e (modelo 55) com suporte a namespace
- ✅ Cálculo automático de base IBS/CBS com fórmula configurável
- ✅ Comparação inteligente com tolerância absoluta e percentual
- ✅ Extração de IBS/CBS do XML via XPath configurável
- ✅ Geração de relatório Excel com 4 abas formatadas:
  - Resumo NF (consolidado por nota)
  - Itens (detalhamento completo)
  - Divergências (filtrado)
  - Erros (XMLs com falha)
- ✅ Processamento paralelo opcional (multi-threading)
- ✅ Barra de progresso (tqdm) para acompanhamento
- ✅ Sistema de configuração via YAML
- ✅ CLI completo com múltiplos argumentos
- ✅ Logs detalhados em arquivo e console
- ✅ Suporte a componentes opcionais da base:
  - vFrete, vSeg, vOutro, vDesc
  - vIPI, vII, vICMSST, vFCPST
  - vPIS, vCOFINS
- ✅ Tratamento robusto de erros
- ✅ Testes unitários (parser, calculator, comparator)
- ✅ Documentação completa (README, QUICKSTART)
- ✅ Exemplos de configuração

#### Características Técnicas
- Python 3.11+
- Type hints completos
- Dataclasses para modelos
- Decimal para precisão numérica
- lxml para parse XML
- pandas + openpyxl para Excel
- Arquitetura modular e extensível

#### Requisitos
- lxml >= 4.9.0
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- pyyaml >= 6.0
- tqdm >= 4.65.0
- python-dateutil >= 2.8.0

---

## Futuras Melhorias Planejadas

### [1.1.0] - Planejado
- [ ] Interface gráfica (GUI) com tkinter ou PyQt
- [ ] Suporte a outros modelos de NF-e (NFC-e, etc.)
- [ ] Export para CSV adicional
- [ ] Dashboard HTML interativo
- [ ] Validação de regras de negócio customizadas
- [ ] Integração com APIs da SEFAZ
- [ ] Cache de XMLs processados
- [ ] Modo incremental (processar apenas novos)

### [1.2.0] - Planejado
- [ ] Suporte a CTe, MDFe
- [ ] Análise estatística avançada
- [ ] Gráficos e visualizações
- [ ] Webhook notifications
- [ ] Docker container
- [ ] API REST

---

## Como Contribuir

Veja o arquivo [README.md](README.md) para instruções sobre como contribuir com o projeto.
