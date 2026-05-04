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
- Análise de churn da rede (comparativo ano a ano)

**Mix de programação**

- Distribuição de tipos de conteúdo por ano
- Evolução temporal do mix editorial
- Categorias: Comissão, Plenário, Audiência Pública, Ordem do Dia, Institucional, entre outras

**Outputs gerados**

- 17 visualizações (PNG)
- 15+ tabelas (CSV/XLSX)
- 1 relatório analítico completo com frases prontas para apresentação (TXT)

---

## Escala atual de uso

| Indicador             | Valor                  |
| --------------------- | ---------------------- |
| Registros analisados  | 22.886+                |
| Emissoras monitoradas | 274 (histórico total)  |
| Municípios alcançados | até 290 de 295 em SC   |
| Período               | 2023–2026              |

---

## Tecnologias

- Python 3.10+
- pandas, matplotlib, seaborn, plotly
- geopandas (mapa coroplético — opcional)
- openpyxl (leitura de arquivos .xlsx)
- Integração com API do IBGE (cache local automático)
- Execução local, sem dependência de servidores externos

---

## Estrutura de arquivos

```
analise_alesc.py              # script principal de análise
auditoria.py                  # validação e auditoria dos dados de entrada
mapa_comercial.py             # mapa interativo de abrangência por comercial
mapa_interativo_intensidade.py # mapa interativo de intensidade de veiculação
data/
  ├── cache/                  # cache automático da API do IBGE
  └── [arquivos de entrada por mês/ano — não incluídos no repositório]
outputs/
  ├── *.png                   # gráficos
  ├── *.csv / *.xlsx          # tabelas
  └── relatorio_analitico.txt
```

---

## Como executar

```bash
# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install pandas matplotlib seaborn plotly geopandas openpyxl requests

# Colocar os arquivos de dados na pasta data/
# Executar
python analise_alesc.py
```

Os outputs são gerados automaticamente na pasta `outputs/`.

---

## Dados de entrada

Os arquivos de dados reais não estão incluídos neste repositório por conterem informações operacionais da instituição.

O sistema foi desenvolvido para dados exportados de plataforma de gerenciamento de broadcast. Para adaptar a outra fonte de dados, ajuste o bloco de ingestão no início do script (colunas `Radio`, `Cidade`, `Tipo`, `Data`, `Comercial`).

---

## Scripts utilitários

**`auditoria.py`** — valida os dados de entrada, detecta inconsistências e gera relatório de validação antes da análise principal.

**`mapa_comercial.py`** — gera mapa interativo de abrangência para um comercial específico, cruzando a rede de emissoras com os municípios cobertos por cada rádio.

**`mapa_interativo_intensidade.py`** — gera mapa interativo de intensidade de veiculação por município, com camada de população e destaque para lacunas estratégicas.

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

---

## Autor

Desenvolvido por **Rodolfo Zalzwedel Espínola**  
Jornalista e produtor — Rádio ALESC / Assembleia Legislativa de Santa Catarina

---

## English summary

**Brazilian legislative radio network analysis system** — territorial coverage, content mix, and partner retention analytics for public broadcasters.

This tool processes broadcast distribution data from radio networks affiliated with Brazilian legislative institutions. It produces territorial coverage maps, audience reach estimates (cross-referenced with IBGE census data), content mix analysis, and partner churn metrics — all as automated outputs from a single Python script.

Built for [Rádio ALESC](https://www.alesc.sc.gov.br/radio), the radio station of the Santa Catarina State Legislative Assembly, Brazil.

**Scale:** 22,886+ broadcast records · 274 partner stations · up to 290 municipalities across Santa Catarina state · 2023–2026

For international inquiries or commercial licensing outside Brazil: rzespinola@gmail.com
