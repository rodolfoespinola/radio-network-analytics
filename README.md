# radio-network-analytics

Territorial coverage, content mix, and partner retention analytics for public radio broadcast networks.

Built for [Rádio ALESC](https://www.alesc.sc.gov.br/radio), the radio station of the Santa Catarina State Legislative Assembly, Brazil.

---

## What this system does

Starting from broadcast distribution data exported by media management platforms, the system automatically produces:

**Territorial analysis**

- Choropleth map of Santa Catarina with per-municipality coverage
- Population reach cross-referenced with IBGE census data
- Territorial Gini index (concentration vs. distribution)
- Strategic gap identification (high-population municipalities with no coverage)
- Broadcast intensity index per capita

**Network analysis**

- Ranking of most active stations by period
- Partner fidelity and retention rate
- Annual movement: new stations, departures, and returns
- Year-over-year churn analysis

**Content mix**

- Distribution of content types by year
- Editorial mix evolution over time
- Categories: Committee, Plenary, Public Hearing, Session, Institutional, and others

**Generated outputs**

- 17 charts (PNG)
- 15+ tables (CSV/XLSX)
- 1 full analytical report with ready-to-present phrases (TXT)

---

## Scale

| Indicator             | Value                       |
| --------------------- | --------------------------- |
| Records analyzed      | 22,886+                     |
| Partner stations      | 274 (total historical)      |
| Municipalities reached| up to 290 of 295 in SC      |
| Period                | 2023–2026                   |

---

## Stack

- Python 3.10+
- pandas, matplotlib, seaborn, plotly
- geopandas (choropleth map — optional)
- openpyxl (xlsx ingestion)
- IBGE Census API with automatic local cache
- Runs fully local, no external server required

---

## File structure

```
analise_alesc.py               # main analysis script
auditoria.py                   # data validation and audit
relatorio_mensal_html.py       # monthly HTML report + PNG for WhatsApp
gerar_mapas_mes.py             # top-3 commercial coverage maps for the month
mapa_comercial.py              # interactive coverage map per broadcast (library + interactive mode)
mapa_interativo_intensidade.py # interactive broadcast intensity map
data/
  ├── radios_municipios_*.csv  # signal coverage mapping per station
  ├── cache/                   # automatic IBGE API cache
  └── [monthly input files — not included in this repository]
outputs/
  ├── dataset_consolidado.csv          # consolidated broadcast dataset
  ├── ranking_impacto_alesc_auditado.csv
  ├── relatorio_radio_alesc_*.html     # monthly reports
  ├── relatorio_radio_alesc_*.png      # PNG exports for WhatsApp
  ├── mapa_comercial_TOP*_*.html       # top-3 commercial coverage maps
  ├── *.png                            # charts
  └── *.csv / *.xlsx                   # tables
```

---

## How to run

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas matplotlib seaborn plotly geopandas openpyxl requests

# Place input data files in data/
python analise_alesc.py
```

Outputs are generated automatically in the `outputs/` folder.

---

## Input data

Real broadcast data files are not included in this repository. The system was built for data exported from a broadcast management platform. To adapt it to a different data source, adjust the ingestion block at the top of the script (columns `Radio`, `Cidade`, `Tipo`, `Data`, `Comercial`).

---

## Monthly workflow

### 1. Monthly HTML report

Generates a full HTML report for a given month, with charts, tables, and reach statistics.

```bash
cd ~/coding/radio_alesc
source radio/bin/activate

# Interactive menu (lists available months)
python3 relatorio_mensal_html.py

# Specific month
python3 relatorio_mensal_html.py --mes 2026-05

# Specific month + PNG export for WhatsApp
python3 relatorio_mensal_html.py --mes 2026-05 --imagem
```

The `--imagem` flag renders a compact layout optimized for mobile (800 px → scaled to 1280 px HD) using Firefox in headless mode. Requires Firefox installed and the `Pillow` package (`pip install Pillow`).

Output: `outputs/relatorio_radio_alesc_mai_2026.html` (and `.png` if `--imagem`).

---

### 2. Top-3 commercial coverage maps

Ranks all commercials aired in the month by population reach and generates interactive HTML maps for the top 3.

```bash
cd ~/coding/radio_alesc
source radio/bin/activate

# Previous month (default)
python3 gerar_mapas_mes.py

# Specific month
python3 gerar_mapas_mes.py --mes 2026-05
```

Output: `outputs/mapa_comercial_TOP1_MAI2026_*.html`, `TOP2`, `TOP3` — all opened in the browser automatically.

---

## Utility scripts

**`auditoria.py`** — validates input data, detects inconsistencies, and generates a validation report before the main analysis runs.

**`mapa_comercial.py`** — interactive coverage map for a specific broadcast (search by name). Also used as a library by `gerar_mapas_mes.py`.

**`mapa_interativo_intensidade.py`** — interactive broadcast intensity map by municipality, with a population layer and strategic gap highlighting.

---

## Applicability

This system can be adapted for any institution distributing content via a partner station network, including:

- State legislative assemblies
- Municipal councils with radio programming
- Public communication agencies
- Media outlets with affiliate networks

---

## License

**Free for non-commercial use** — this code may be used, studied, and adapted for educational, academic, and portfolio purposes without restrictions.

**Commercial use** (institutional deployment, service delivery, derivative products) requires prior authorization from the author.

---

## Author

**Rodolfo Zalzwedel Espínola**  
Journalist and producer — Rádio ALESC / Santa Catarina State Legislative Assembly, Brazil

---

## Versão em português

Sistema de análise de dados para emissoras de rádio parceiras de instituições públicas, com foco em cobertura territorial, mix de programação e dinâmica de rede. Desenvolvido para a Rádio ALESC, veículo de comunicação da Assembleia Legislativa de Santa Catarina.

Produz automaticamente mapas, tabelas e relatório analítico a partir de dados de veiculação exportados de plataformas de gestão de broadcast. Escala atual: 22.886+ registros, 274 emissoras monitoradas, até 290 municípios de SC, período 2023–2026.

Para consultas comerciais: rzespinola@gmail.com
