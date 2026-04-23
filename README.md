# Rádio ALESC — Sistema de Análise de Distribuição e Cobertura

Sistema de análise de dados para emissoras de rádio parceiras de instituições públicas, com foco em cobertura territorial, mix de programação e dinâmica de rede.

Desenvolvido para a [Rádio ALESC](https://www.alesc.sc.gov.br/radio), veículo de comunicação da Assembleia Legislativa de Santa Catarina.

---

## O que este sistema faz

A partir de dados de veiculação exportados por plataformas de gerenciamento de broadcast, o sistema produz automaticamente:

**Análise territorial**

- Mapa coroplético de SC com cobertura por município
- Cobertura populacional cruzada com dados do IBGE
- Índice de Gini territorial (concentração vs. distribuição)
- Identificação de lacunas estratégicas (municípios populosos sem cobertura)
- Índice de intensidade de veiculação por habitante

**Análise da rede de emissoras**

- Ranking das rádios mais ativas por período
- Taxa de fidelidade e retenção de parceiros
- Movimentação anual: novas emissoras, saídas, retornos
- Análise de churn da rede

**Mix de programação**

- Distribuição de tipos de conteúdo por ano
- Evolução temporal do mix editorial
- Categorias: Comissão, Plenário, Audiência Pública, Ordem do Dia, Institucional, entre outras

**Outputs gerados**

- 15 visualizações (PNG)
- 12 tabelas (CSV)
- 1 relatório analítico completo com frases prontas para apresentação (TXT)

---

## Escala atual de uso

| Indicador             | Valor            |
| --------------------- | ---------------- |
| Registros analisados  | 21.952+          |
| Emissoras monitoradas | 302              |
| Municípios cobertos   | 116 de 295 em SC |
| Período               | 2023–2026        |

---

## Tecnologias

- Python 3.10+
- pandas, matplotlib, seaborn, plotly
- Integração com API do IBGE (cache local automático)
- Execução local, sem dependência de servidores externos

---

## Estrutura de arquivos

```
analise_alesc_final.py   # script principal
data/
  ├── cache/             # cache automático da API do IBGE
  └── [arquivos de entrada por ano]
outputs/
  ├── *.png              # gráficos
  ├── *.csv              # tabelas
  └── relatorio_analitico.txt
```

---

## Como executar

```bash
# Instalar dependências
pip install pandas matplotlib seaborn plotly requests

# Colocar os arquivos de dados na pasta data/
# Executar
python analise_alesc_final.py
```

Os outputs são gerados automaticamente na pasta `outputs/`.

---

## Dados de entrada

O sistema foi desenvolvido para dados exportados de plataforma de gerenciamento de broadcast. Os dados de exemplo incluídos neste repositório são **sintéticos**, gerados para fins de demonstração.

Para adaptar o sistema a outra fonte de dados, é necessário ajustar o bloco de ingestão no início do script (colunas `Radio`, `Cidade`, `Tipo`, `Data`, `Comercial`).

---

## Aplicabilidade

Este sistema pode ser adaptado para qualquer instituição que distribua conteúdo via rede de emissoras parceiras, incluindo:

- Assembleias legislativas estaduais
- Câmaras municipais com programação em rádio
- Agências de comunicação pública
- Veículos com rede de afiliadas

---

## Licença

**Uso não-comercial livre** — este código pode ser usado, estudado e adaptado para fins educacionais, acadêmicos e de portfólio sem restrições.

**Uso comercial** (implantação em instituições, prestação de serviços, produtos derivados) requer autorização prévia do autor.

Para consultas comerciais: [seu contato aqui]

---

## Autor

Desenvolvido por **Rodolfo Zalzwedel Espínola**  
Jornalista e produtor — Rádio ALESC / Assembleia Legislativa de Santa Catarina  
[LinkedIn] · [contato]

---

## English summary

**Brazilian legislative radio network analysis system** — territorial coverage, content mix, and partner retention analytics for public broadcasters.

This tool processes broadcast distribution data from radio networks affiliated with Brazilian legislative institutions. It produces territorial coverage maps, audience reach estimates (cross-referenced with IBGE census data), content mix analysis, and partner churn metrics — all as automated outputs from a single Python script.

Built for [Rádio ALESC](https://www.alesc.sc.gov.br/radio), the radio station of the Santa Catarina State Legislative Assembly, Brazil.

**Scale:** 21,952+ broadcast records · 302 partner stations · 116 municipalities across Santa Catarina state · 2023–2026

For international inquiries or commercial licensing outside Brazil: [your contact here]
