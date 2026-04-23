# auditar_ranking.py
import pandas as pd
import unicodedata
import re
from pathlib import Path

# ── Mesmas funções do script principal ────────────────────────────────────────
def normalizar(texto):
    if pd.isna(texto): return ""
    texto = str(texto).lower().strip().replace("-", " ").replace("'", " ")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def normalizar_radio(texto):
    if pd.isna(texto): return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto)

# ── Carrega dataset consolidado (já gerado pelo script principal) ──────────────
df = pd.read_csv("outputs/dataset_consolidado.csv", encoding="utf-8-sig", low_memory=False)
df["Radio_norm"] = df["Radio"].apply(normalizar_radio)

# ── Carrega ranking novo ──────────────────────────────────────────────────────
ranking = pd.read_csv("outputs/ranking_impacto_alesc_auditado.csv")

# ── Carrega CSV de abrangência ────────────────────────────────────────────────
for nome in ["data/radios_municipios_-_mar2026.csv", "data/radios municipios - mar2026.csv"]:
    if Path(nome).exists():
        raw_abr = pd.read_csv(nome, encoding="utf-8", sep=None, engine="python", header=None)
        break

mapa_abrangencia = {}
for _, row in raw_abr.iterrows():
    radio_raw = str(row.iloc[0]).strip()
    if not radio_raw or radio_raw == "nan": continue
    rn = normalizar_radio(radio_raw)
    cidades = [normalizar(str(v).split("/")[0].strip())
               for v in row.iloc[1:]
               if pd.notna(v) and str(v).strip() not in ("nan","")]
    if cidades:
        mapa_abrangencia[rn] = set(cidades)

# ── Carrega população ─────────────────────────────────────────────────────────
# Recalcula Cidade_norm a partir da coluna Cidade (que existe no export)
df_pop_raw = pd.read_csv("outputs/dataset_consolidado.csv", encoding="utf-8-sig",
                         usecols=["Cidade","Populacao"], low_memory=False)
df_pop_raw["Cidade_norm"] = df_pop_raw["Cidade"].apply(normalizar)
df_pop = (df_pop_raw.dropna(subset=["Cidade_norm","Populacao"])
                    .drop_duplicates(subset=["Cidade_norm"])
                    .copy())

# E o df principal também precisa de Cidade_norm
df["Cidade_norm"] = df["Cidade"].apply(normalizar)

# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIA INTERATIVA
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("AUDITORIA DO RANKING DE IMPACTO")
print("="*70)

# Mostra conteúdos com 1 ou 2 emissoras para escolher um caso simples
print("\nConteúdos com 1-2 emissoras (mais fáceis de auditar):")
simples = ranking[ranking["Emissoras"] <= 2].sort_values("Populacao", ascending=False).head(15)
print(simples[["Conteudo","Populacao","Cidades","Emissoras"]].to_string(index=False))

print("\n" + "-"*70)
conteudo_teste = input("\nDigite o nome EXATO do conteúdo para auditar (ou Enter para o #1 acima): ").strip()
if not conteudo_teste:
    conteudo_teste = simples.iloc[0]["Conteudo"]

print(f"\n{'='*70}")
print(f"AUDITANDO: {conteudo_teste}")
print(f"{'='*70}")

# 1. O que o ranking diz
linha_ranking = ranking[ranking["Conteudo"] == conteudo_teste]
if linha_ranking.empty:
    print("⚠ Conteúdo não encontrado no ranking.")
else:
    print("\n[RANKING CALCULOU]")
    print(linha_ranking[["Conteudo","Populacao","Cidades","Emissoras"]].to_string(index=False))

# 2. Quais rádios veicularam e em quais cidades
veiculacoes = df[df["Comercial"] == conteudo_teste][["Radio","Cidade"]].drop_duplicates()
print(f"\n[VEICULAÇÕES DIRETAS — {len(veiculacoes)} registros]")
print(veiculacoes.to_string(index=False))

# 3. Expansão por abrangência — recalcula na mão
municipios_total = set()
mapa_sede = df.groupby("Radio_norm")["Cidade_norm"].first().to_dict()

radios_do_conteudo = df[df["Comercial"] == conteudo_teste]["Radio_norm"].dropna().unique()
print(f"\n[EXPANSÃO POR ABRANGÊNCIA — {len(radios_do_conteudo)} rádios]")

for rn in sorted(radios_do_conteudo):
    radio_display = df[df["Radio_norm"] == rn]["Radio"].iloc[0]
    if rn in mapa_abrangencia:
        munis = mapa_abrangencia[rn]
        municipios_total.update(munis)
        print(f"  ✓ {radio_display:<45} → {len(munis):3d} municípios no sinal")
    else:
        sede = mapa_sede.get(rn, "")
        if sede:
            municipios_total.add(sede)
        print(f"  ⚠ {radio_display:<45} → sem mapeamento (fallback: {sede})")

# Adiciona veiculações diretas
cids_diretas = set(df[df["Comercial"] == conteudo_teste]["Cidade_norm3].dropna().unique())
municipios_total.update(cids_diretas)

# 4. Recalcula população
pop_recalculada = df_pop[df_pop["Cidade_norm"].isin(municipios_total)]["Populacao"].sum()

print(f"\n[RESULTADO RECALCULADO MANUALMENTE]")
print(f"  Municípios únicos na união: {len(municipios_total)}")
print(f"  População total:            {int(pop_recalculada):,}")
print(f"  Bate com o ranking?         {'✓ SIM' if abs(pop_recalculada - linha_ranking['Populacao'].iloc[0]) < 1000 else '✗ NÃO — diferença: ' + str(int(pop_recalculada - linha_ranking['Populacao'].iloc[0]))}")

print(f"\n[MUNICÍPIOS INCLUÍDOS]")
print(sorted(municipios_total))