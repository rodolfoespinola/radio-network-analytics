# -*- coding: utf-8 -*-
"""
gerar_mapas_mes.py — Gera automaticamente os mapas dos 3 comerciais com maior
população alcançada em um mês específico.

Uso:
    python gerar_mapas_mes.py              # mês anterior (padrão)
    python gerar_mapas_mes.py --mes 2026-04

Saída: outputs/mapa_comercial_TOP1_ABR2026_*.html  (e TOP2, TOP3)
Os três mapas são abertos automaticamente no navegador.
"""

import argparse
from datetime import date, timedelta
import pandas as pd

# ── Argumento de mês ──────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument(
    "--mes",
    help="Mês a analisar no formato YYYY-MM (padrão: mês anterior)",
    default=None,
)
args = parser.parse_args()

if args.mes:
    try:
        ano, mes = map(int, args.mes.split("-"))
    except ValueError:
        print("Formato inválido. Use --mes YYYY-MM  (ex: --mes 2026-04)")
        raise SystemExit
else:
    hoje = date.today().replace(day=1)
    mes_anterior = (hoje - timedelta(days=1)).replace(day=1)
    ano, mes = mes_anterior.year, mes_anterior.month

MESES_PT = {
    1: "JAN", 2: "FEV", 3: "MAR", 4: "ABR",
    5: "MAI", 6: "JUN", 7: "JUL", 8: "AGO",
    9: "SET", 10: "OUT", 11: "NOV", 12: "DEZ",
}
rotulo_mes = f"{MESES_PT[mes]}{ano}"

print("=" * 70)
print(f"MAPAS TOP 3 — {MESES_PT[mes]}/{ano}")
print("=" * 70)

# ── Importa dados e função do mapa_comercial ─────────────────────────────────
print("\nCarregando dados (mapa_comercial)...")
import mapa_comercial as mc

df = mc.df

# ── Filtra pelo mês ───────────────────────────────────────────────────────────
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
df_mes = df[(df["Data"].dt.year == ano) & (df["Data"].dt.month == mes)].copy()

if df_mes.empty:
    print(f"\nNenhum registro encontrado para {MESES_PT[mes]}/{ano}.")
    print("Verifique se o dataset foi gerado com dados deste mês.")
    raise SystemExit

n_total = len(df_mes)
n_comerciais = df_mes["Comercial"].nunique()
print(f"  {n_total:,} veiculações  ·  {n_comerciais} comerciais distintos em {MESES_PT[mes]}/{ano}")

# ── Calcula população alcançada por comercial no mês ─────────────────────────
print("\nCalculando população alcançada por comercial...")

registros_pop = []
for comercial, grupo in df_mes.groupby("Comercial"):
    if pd.isna(comercial) or not str(comercial).strip():
        continue

    radios = set(grupo["Radio_norm"].dropna().unique())
    municipios = set(grupo["Cidade_norm"].dropna().unique()) - {""}

    for rn in radios:
        if rn in mc.mapa_abrangencia:
            municipios.update(mc.mapa_abrangencia[rn])
        else:
            sede = mc.mapa_sede.get(rn, "")
            if sede:
                municipios.add(sede)

    municipios -= {""}

    pop = 0
    for cn in municipios:
        pop_ds = mc.df_pop.loc[mc.df_pop["Cidade_norm"] == cn, "Populacao"]
        if not pop_ds.empty:
            pop += int(pop_ds.iloc[0])

    registros_pop.append({
        "Comercial":   comercial,
        "Pop_Alcance": pop,
        "Veiculacoes": len(grupo),
    })

if not registros_pop:
    print("Nenhum comercial com dados suficientes para ranquear.")
    raise SystemExit

ranking_mes = (
    pd.DataFrame(registros_pop)
    .sort_values("Pop_Alcance", ascending=False)
    .reset_index(drop=True)
)

print(f"\nTop 10 por população alcançada em {MESES_PT[mes]}/{ano}:")
for i, row in ranking_mes.head(10).iterrows():
    nome_curto = row["Comercial"][:60] + "..." if len(row["Comercial"]) > 60 else row["Comercial"]
    print(f"  {i+1:2d}. {nome_curto}")
    print(f"      Pop. alcançada: {row['Pop_Alcance']:,.0f} hab.  ·  {row['Veiculacoes']} veiculações")

# ── Gera os 3 mapas ───────────────────────────────────────────────────────────
top3 = ranking_mes.head(3)

print(f"\nGerando {len(top3)} mapas...")
caminhos = []
for posicao, (_, row) in enumerate(top3.iterrows(), start=1):
    sufixo = f"TOP{posicao}_{rotulo_mes}_"
    caminho = mc.gerar_mapa(
        conteudo=row["Comercial"],
        sufixo=sufixo,
        n_veic_mes=int(row["Veiculacoes"]),
        abrir_navegador=False,
    )
    if caminho:
        caminhos.append(caminho)

# Abre todos de uma vez no navegador
import webbrowser
for caminho in caminhos:
    webbrowser.open(caminho.resolve().as_uri())

print(f"\n✓ {len(caminhos)} mapa(s) gerado(s) e abertos no navegador.")
print(f"  Arquivos em: outputs/mapa_comercial_TOP*_{rotulo_mes}_*.html")
