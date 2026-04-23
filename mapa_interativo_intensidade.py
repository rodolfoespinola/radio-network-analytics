import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import unicodedata
import numpy as np
from io import StringIO
from pathlib import Path

OUTPUT_DIR = Path("/mnt/user-data/outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

CENTROIDES_CSV = """municipio,lat,lon,pop
Abdon Batista,-27.6097,-51.0228,2425
Abelardo Luz,-26.5697,-52.3261,17089
Agrolândia,-27.4058,-49.8236,10260
Agronômica,-27.2728,-49.8583,5131
Água Doce,-26.9944,-51.5531,6975
Águas de Chapecó,-27.1844,-52.9878,6108
Águas Frias,-26.8644,-52.7278,2407
Águas Mornas,-27.7069,-48.8286,5801
Alfredo Wagner,-27.6947,-49.3358,9482
Alto Bela Vista,-27.3722,-52.0047,2150
Anchieta,-26.5328,-53.3378,6188
Angelina,-27.5750,-48.9964,5123
Anita Garibaldi,-27.6947,-51.1303,9096
Anitápolis,-27.9056,-49.1278,3292
Antônio Carlos,-27.4650,-48.7508,11024
Apiúna,-27.0397,-49.3872,9867
Arabutã,-27.1556,-52.1539,4229
Araquari,-26.3761,-48.7214,40890
Araranguá,-28.9347,-49.4861,70386
Armazém,-28.2547,-49.0128,8244
Arroio Trinta,-26.9281,-51.3428,3547
Arvoredo,-27.0425,-52.2889,1980
Ascurra,-26.9747,-49.3694,9600
Atalanta,-27.3828,-49.7878,3487
Aurora,-27.3097,-49.6378,5617
Balneário Arroio do Silva,-28.9833,-49.4083,12283
Balneário Barra do Sul,-26.4572,-48.6108,13373
Balneário Camboriú,-26.9903,-48.6347,138732
Balneário Gaivota,-29.1167,-49.5833,10547
Balneário Piçarras,-26.7603,-48.6708,23204
Balneário Rincão,-28.8333,-49.2500,12081
Bandeirante,-26.5828,-53.5714,2928
Barra Bonita,-26.6033,-53.4944,1896
Barra Velha,-26.6328,-48.6839,29084
Bela Vista do Toldo,-26.0528,-50.4778,6222
Belmonte,-26.5044,-53.4717,2048
Benedito Novo,-26.7833,-49.3728,11618
Biguaçu,-27.4939,-48.6558,70471
Blumenau,-26.9194,-49.0661,361855
Bocaina do Sul,-27.7394,-50.0044,3017
Bom Jardim da Serra,-28.3342,-49.6258,4536
Bom Jesus,-26.7522,-52.3894,2418
Bom Jesus do Oeste,-26.7089,-53.0778,2185
Bom Retiro,-27.7961,-49.4892,9548
Bombinhas,-27.1417,-48.5153,17583
Botuverá,-27.2028,-49.0742,5178
Braço do Norte,-28.2742,-49.1647,32244
Braço do Trombudo,-27.3189,-49.9200,4264
Brunópolis,-27.3344,-51.0889,2851
Brusque,-27.0990,-48.9167,133424
Caçador,-26.7753,-51.0144,77088
Caibi,-27.0628,-53.2453,6040
Calmon,-26.5344,-51.0378,3779
Camboriú,-27.0228,-48.6558,87179
Campo Alegre,-26.1997,-49.2644,11941
Campo Belo do Sul,-27.8942,-50.7644,7400
Campo Erê,-26.3917,-53.0878,9016
Campos Novos,-27.4025,-51.2253,32972
Canelinha,-27.2694,-48.7747,11823
Canoinhas,-26.1806,-50.3900,53569
Capão Alto,-28.0208,-50.5011,3134
Capinzal,-27.3408,-51.6158,23450
Capivari de Baixo,-28.4458,-49.0011,24022
Catanduvas,-27.0728,-51.6578,9773
Caxambu do Sul,-27.1503,-52.8644,5003
Celso Ramos,-27.6286,-51.3017,2768
Cerro Negro,-27.7700,-50.8700,3407
Chapadão do Lageado,-27.5628,-49.6997,2140
Chapecó,-27.1003,-52.6150,236582
Cocal do Sul,-28.6025,-49.3258,16432
Concórdia,-27.2342,-52.0278,75035
Cordilheira Alta,-27.2028,-52.6489,5300
Coronel Freitas,-26.9044,-52.7214,10200
Coronel Martins,-26.5514,-52.6289,2800
Correia Pinto,-27.5858,-50.3608,15447
Corupá,-26.4264,-49.2411,14672
Criciúma,-28.6775,-49.3697,224574
Cunha Porã,-26.8931,-53.1736,13150
Cunhataí,-26.9439,-53.1178,2400
Curitibanos,-27.2825,-50.5831,40591
Descanso,-26.8228,-53.5017,9000
Dionísio Cerqueira,-26.2550,-53.6369,14700
Dona Emma,-26.9294,-49.5208,3900
Doutor Pedrinho,-26.7422,-49.4783,3500
Entre Rios,-26.7044,-52.5528,3800
Ermo,-28.9894,-49.6814,2200
Erval Velho,-27.2797,-51.4539,4800
Faxinal dos Guedes,-26.8500,-52.2581,9500
Flor do Sertão,-26.7044,-53.4028,1800
Florianópolis,-27.5954,-48.5480,516524
Formosa do Sul,-26.6578,-52.8578,2500
Forquilhinha,-28.7453,-49.4728,26900
Fraiburgo,-27.0228,-50.9192,38065
Frei Rogério,-27.1736,-50.8278,3200
Galvão,-26.4339,-52.5578,3900
Garopaba,-28.0239,-48.6228,22300
Garuva,-26.0331,-48.8508,17500
Gaspar,-26.9314,-48.9578,72530
Governador Celso Ramos,-27.3183,-48.5578,13000
Grão Pará,-28.1764,-49.2297,6800
Gravatal,-28.3228,-49.0458,11400
Guabiruba,-27.0636,-48.9836,22500
Guaraciaba,-26.5947,-53.5228,10400
Guaramirim,-26.4728,-48.9978,46757
Guarujá do Sul,-26.3828,-53.5194,5000
Guatambú,-27.1506,-52.7983,5000
Herval d'Oeste,-27.1906,-51.4869,22000
Ibiam,-27.2653,-51.4808,2200
Ibicaré,-27.0819,-51.3517,3200
Ibirama,-27.0572,-49.5178,18100
Içara,-28.7133,-49.3036,58055
Ilhota,-26.8994,-48.8283,13300
Imaruí,-28.3292,-48.8197,11600
Imbituba,-28.2406,-48.6658,46600
Imbuia,-27.4878,-49.5228,5300
Indaial,-26.8978,-49.2333,68000
Iomerê,-27.0022,-51.2428,2800
Ipira,-27.3978,-51.7878,4100
Iporã do Oeste,-26.9978,-53.5325,8000
Ipuaçu,-26.6428,-52.4678,7400
Ipumirim,-27.0714,-52.0928,8000
Iraceminha,-26.8228,-53.2778,4500
Irani,-27.0303,-51.8717,9800
Irati,-26.5344,-52.4678,3800
Irineópolis,-26.2344,-50.7894,10200
Itá,-27.2906,-52.3244,5200
Itaiópolis,-26.3378,-49.9083,22700
Itajaí,-26.9078,-48.6619,223118
Itapema,-27.0861,-48.6147,64400
Itapiranga,-27.1681,-53.7108,16700
Itapoá,-26.1244,-48.6139,24100
Ituporanga,-27.4128,-49.5978,25000
Jaborá,-27.1797,-51.7378,3600
Jacinto Machado,-28.9981,-49.7614,11200
Jaguaruna,-28.6128,-49.0297,19900
Jaraguá do Sul,-26.4853,-49.0689,177800
Jardinópolis,-26.7228,-52.9278,2500
Joaçaba,-27.1742,-51.5044,27200
Joinville,-26.3044,-48.8487,616526
José Boiteux,-27.0028,-49.6478,4800
Jupiá,-26.4144,-52.9028,2400
Lacerdópolis,-27.2497,-51.5544,2100
Lages,-27.8158,-50.3258,157925
Laguna,-28.4808,-48.7811,52600
Lajeado Grande,-26.7678,-52.4878,2300
Laurentino,-27.2233,-49.7378,6500
Lauro Müller,-28.3892,-49.3997,14700
Lebon Régis,-26.9256,-50.6917,11500
Leoberto Leal,-27.6219,-49.1528,3900
Lindóia do Sul,-27.0519,-52.1497,3900
Lontras,-27.1578,-49.5303,10700
Luiz Alves,-26.7158,-48.9250,10900
Luzerna,-27.1294,-51.4742,5000
Macieira,-26.7906,-51.3128,2200
Mafra,-26.1097,-49.8019,58400
Major Gercino,-27.4361,-48.9119,3000
Major Vieira,-26.3694,-50.3233,8700
Maracajá,-28.8328,-49.4458,7100
Maravilha,-26.7692,-53.1717,25000
Marema,-26.9044,-52.5878,2300
Massaranduba,-26.6086,-49.0075,16700
Matos Costa,-26.4728,-51.1544,3100
Meleiro,-28.8278,-49.6358,7700
Mirim Doce,-27.1611,-50.0867,2500
Modelo,-26.7819,-53.0239,5200
Mondaí,-27.0975,-53.4044,11300
Monte Carlo,-27.2278,-50.9628,3900
Monte Castelo,-26.4578,-50.2244,8800
Morro da Fumaça,-28.6544,-49.2278,17400
Morro Grande,-28.7667,-49.7000,3200
Navegantes,-26.8994,-48.6539,85734
Nova Erechim,-26.9000,-52.9097,8900
Nova Itaberaba,-26.9406,-52.8408,4200
Nova Trento,-27.2883,-48.9278,13600
Nova Veneza,-28.6381,-49.5025,14500
Novo Horizonte,-26.4578,-52.8100,3400
Orleans,-28.3600,-49.2958,21700
Otacílio Costa,-27.4786,-50.1228,18900
Ouro,-27.3544,-51.6178,7200
Ouro Verde,-26.6978,-52.3028,4100
Paial,-27.2478,-52.4378,1900
Painel,-28.0019,-50.1006,2400
Palhoça,-27.6447,-48.6658,178679
Palma Sola,-26.3525,-53.2869,7900
Palmeira,-27.9236,-50.1583,5100
Palmitos,-27.0711,-53.1578,17400
Papanduva,-26.3822,-50.1478,20500
Paraíso,-26.6111,-53.2897,4200
Passo de Torres,-29.3244,-49.7178,7500
Passos Maia,-26.7844,-51.9244,3800
Paulo Lopes,-27.9617,-48.6808,7200
Pedras Grandes,-28.4489,-49.1900,4100
Penha,-26.7711,-48.6447,26400
Peritiba,-27.4278,-51.9428,3600
Pescaria Brava,-28.3833,-48.8667,14000
Petrolândia,-27.5317,-49.6878,9800
Pinhalzinho,-26.8472,-52.9869,23200
Pinheiro Preto,-27.0814,-51.2183,3600
Piratuba,-27.4228,-51.7728,4700
Planalto Alegre,-27.0428,-52.7739,3500
Pomerode,-26.7428,-49.1756,34360
Ponte Alta,-27.4869,-50.3814,6000
Ponte Alta do Norte,-27.1542,-50.4553,3200
Ponte Serrada,-26.8694,-52.0158,9000
Porto Belo,-27.1558,-48.5508,20500
Porto União,-26.2331,-51.0794,34000
Pouso Redondo,-27.2578,-49.9478,14600
Praia Grande,-29.1928,-49.9578,7300
Presidente Castello Branco,-27.1778,-51.7244,1800
Presidente Getúlio,-27.0478,-49.6247,14900
Presidente Nereu,-27.2528,-49.7478,2700
Princesa,-26.4539,-53.5494,2500
Quilombo,-26.7306,-52.7244,12000
Rancho Queimado,-27.6828,-49.0119,3000
Rio das Antas,-26.8942,-51.0817,9800
Rio do Campo,-26.9578,-50.1428,5700
Rio do Oeste,-27.1933,-49.7978,7200
Rio do Sul,-27.2147,-49.6436,71220
Rio dos Cedros,-26.7458,-49.2747,11200
Rio Fortuna,-28.1728,-49.1042,4600
Rio Negrinho,-26.2553,-49.5197,43700
Rio Rufino,-27.8786,-49.9000,2800
Riqueza,-27.0814,-53.3367,4700
Rodeio,-26.9239,-49.3528,11700
Romelândia,-26.6828,-53.3517,5300
Salete,-26.9828,-49.6878,7200
Saltinho,-26.5847,-52.6553,3200
Salto Veloso,-26.9553,-51.2019,4300
Sangão,-28.5656,-49.1264,12100
Santa Cecília,-26.9594,-50.4247,15900
Santa Helena,-26.9378,-53.6183,2700
Santa Rosa de Lima,-28.0356,-49.1378,2200
Santa Rosa do Sul,-29.1244,-49.7358,8900
Santa Terezinha,-26.7806,-50.0278,9800
Santa Terezinha do Progresso,-26.8236,-53.1978,3300
Santiago do Sul,-26.5678,-52.5278,2200
Santo Amaro da Imperatriz,-27.6836,-48.7906,22800
São Bento do Sul,-26.2500,-49.3797,83500
São Bernardino,-26.4528,-52.8778,3100
São Bonifácio,-27.9053,-48.9378,3200
São Carlos,-27.0778,-53.0478,10200
São Cristóvão do Sul,-27.2967,-50.3728,5400
São Domingos,-26.5647,-52.5344,9300
São Francisco do Sul,-26.2433,-48.6397,52400
São João Batista,-27.2728,-48.8483,33300
São João do Itaperiú,-26.6558,-48.7753,5000
São João do Oeste,-27.0903,-53.5581,6400
São João do Sul,-29.2458,-49.8078,7000
São Joaquim,-28.2942,-49.9317,25700
São José,-27.6136,-48.6369,253705
São José do Cedro,-26.4700,-53.5528,14300
São José do Cerrito,-27.6528,-50.5817,9000
São Lourenço do Oeste,-26.3578,-52.8478,22800
São Ludgero,-28.3158,-49.1697,12300
São Martinho,-28.1353,-49.1267,3700
São Miguel da Boa Vista,-26.7539,-53.4017,2400
São Miguel do Oeste,-26.7278,-53.5139,38400
São Pedro de Alcântara,-27.5847,-48.8028,5000
Saudades,-26.9353,-53.0028,9900
Schroeder,-26.4153,-49.0681,17900
Seara,-27.1503,-52.3167,16300
Serra Alta,-26.7278,-52.8678,4100
Siderópolis,-28.5981,-49.4258,14300
Sombrio,-29.1058,-49.6333,30300
Sul Brasil,-26.7214,-52.9678,2600
Taió,-27.1144,-49.9994,19400
Tangará,-27.1022,-51.2494,8500
Tigrinhos,-26.7139,-53.2878,2100
Tijucas,-27.2422,-48.6344,41000
Timbé do Sul,-28.9781,-49.8261,5400
Timbó,-26.8228,-49.2717,47000
Timbó Grande,-26.6144,-50.9028,6800
Três Barras,-26.1208,-50.3133,20200
Treviso,-28.5406,-49.4928,3900
Treze de Maio,-28.5658,-49.1856,7200
Treze Tílias,-26.6044,-51.4017,7200
Tubarão,-28.4678,-49.0128,104659
Tunápolis,-26.9828,-53.6178,4700
Turvo,-28.9258,-49.6897,12200
União do Oeste,-26.7928,-52.8378,2900
Urubici,-28.0158,-49.5919,11200
Urupema,-28.0006,-49.8767,2700
Urussanga,-28.5200,-49.3228,22200
Vargeão,-26.8339,-52.1300,4400
Vargem,-27.5506,-50.8600,3300
Vargem Bonita,-26.9878,-52.0008,4400
Vidal Ramos,-27.3897,-49.3578,7000
Videira,-27.0078,-51.1536,53600
Vitor Meireles,-26.8933,-49.7367,5400
Witmarsum,-27.3278,-49.5578,6000
Xanxerê,-26.8758,-52.4031,47200
Xavantina,-27.0617,-52.3478,5500
Xaxim,-26.9606,-52.5369,26900
Zortéa,-27.4722,-51.5531,4100
"""

def normalizar(texto):
    if not texto: return ""
    texto = str(texto).lower().strip().replace("-"," ").replace("'"," ")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

# ── Carrega dados ──────────────────────────────────────────────────────────────
dfs = []
for arq in sorted(Path("/mnt/user-data/uploads").glob("*.xlsx")):
    try:
        tmp = pd.read_excel(arq, header=None)
        if str(tmp.iloc[0,1]).strip().lower() == "data":
            tmp = tmp.iloc[2:].reset_index(drop=True)
        tmp.columns = ["Identificador","Data","Hora","Radio","Cidade_UF","Peca","Comercial"][:len(tmp.columns)]
        tmp = tmp.dropna(subset=[tmp.columns[0]])
        dfs.append(tmp)
    except: pass

df = pd.concat(dfs, ignore_index=True)
df[["Cidade","UF"]] = df["Cidade_UF"].str.extract(r"^(.+?)\s*/\s*(\w{2})$")
df["Cidade"]      = df["Cidade"].str.strip()
df["Cidade_norm"] = df["Cidade"].apply(normalizar)
df["Data"]        = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce", format="mixed")
df                = df.dropna(subset=["Data"])
df["Ano"]         = df["Data"].dt.year.astype(int)
df                = df[df["Ano"] >= 2020]
mask = df["Comercial"].isna() & df["Peca"].notna()
df.loc[mask, "Comercial"] = df.loc[mask, "Peca"]

anos = sorted(df["Ano"].unique())

# Alcance por município
alcance = (df.groupby(["Cidade","Cidade_norm"])
             .agg(Veiculacoes=("Identificador","count"))
             .reset_index())

# Centroides com população
df_cent = pd.read_csv(StringIO(CENTROIDES_CSV))
df_cent["Cidade_norm"] = df_cent["municipio"].apply(normalizar)

# Merge
mapa = alcance.merge(df_cent[["Cidade_norm","lat","lon","pop"]], on="Cidade_norm", how="left")
mapa = mapa.dropna(subset=["lat","lon","pop"])

# Métricas
mapa["Indice_Intensidade"] = (mapa["Veiculacoes"] / mapa["pop"] * 10_000).round(1)
mapa["Audiencia_Potencial"] = (mapa["pop"] * 0.80).round(0).astype(int)

# Classificação por quartil para o tooltip
q1 = mapa["Indice_Intensidade"].quantile(0.25)
q3 = mapa["Indice_Intensidade"].quantile(0.75)
mediana = mapa["Indice_Intensidade"].median()

def classificar(idx):
    if idx >= q3:   return "🟢 Alta intensidade"
    if idx >= q1:   return "🟡 Intensidade média"
    return              "🔴 Baixa intensidade"

mapa["Classificacao"]      = mapa["Indice_Intensidade"].apply(classificar)
mapa["Veiculacoes_fmt"]    = mapa["Veiculacoes"].apply(lambda x: f"{x:,}".replace(",","."))
mapa["Populacao_fmt"]      = mapa["pop"].apply(lambda x: f"{x:,}".replace(",","."))
mapa["Audiencia_fmt"]      = mapa["Audiencia_Potencial"].apply(lambda x: f"{x:,}".replace(",","."))
mapa["Indice_fmt"]         = mapa["Indice_Intensidade"].apply(lambda x: f"{x:.1f}")

# Cap no p95 para escala de cor não ser distorcida por Itá (484/10k)
vmax_cap = mapa["Indice_Intensidade"].quantile(0.95)
mapa["Indice_cor"] = mapa["Indice_Intensidade"].clip(upper=vmax_cap)

print(f"Municípios: {len(mapa)} | Mediana: {mediana:.1f}/10k | Q1: {q1:.1f} | Q3: {q3:.1f}")

# ── Mapa interativo ────────────────────────────────────────────────────────────
fig = px.scatter_mapbox(
    mapa,
    lat="lat",
    lon="lon",
    size="pop",
    color="Indice_cor",
    hover_name="Cidade",
    hover_data={
        "lat":              False,
        "lon":              False,
        "pop":              False,
        "Indice_cor":       False,
        "Veiculacoes_fmt":  True,
        "Populacao_fmt":    True,
        "Audiencia_fmt":    True,
        "Indice_fmt":       True,
        "Classificacao":    True,
    },
    color_continuous_scale=[
        [0.0,  "#d73027"],   # vermelho — baixa intensidade
        [0.35, "#fc8d59"],   # laranja
        [0.5,  "#fee08b"],   # amarelo — mediana
        [0.65, "#91cf60"],   # verde claro
        [1.0,  "#1a9850"],   # verde escuro — alta intensidade
    ],
    range_color=[0, vmax_cap],
    size_max=50,
    zoom=6.8,
    center={"lat": -27.5, "lon": -50.5},
    mapbox_style="carto-positron",
    title=f"Intensidade de Cobertura — Rádio Alesc ({anos[0]}–{anos[-1]})",
    labels={
        "Veiculacoes_fmt":  "Veiculações",
        "Populacao_fmt":    "População",
        "Audiencia_fmt":    "Audiência potencial",
        "Indice_fmt":       "Índice (/10k hab.)",
        "Classificacao":    "Classificação",
        "Indice_cor":       "Índice de intensidade",
    },
)

fig.update_layout(
    margin={"r": 0, "t": 60, "l": 0, "b": 0},
    paper_bgcolor="#f8f9fa",
    font=dict(family="Arial, sans-serif", size=13),
    title=dict(
        text=(f"<b>Intensidade de Cobertura — Rádio Alesc ({anos[0]}–{anos[-1]})</b><br>"
              "<sup>Tamanho = população  ·  Cor = veiculações por 10.000 hab.  "
              "·  Passe o mouse sobre cada cidade para detalhes</sup>"),
        x=0.5, xanchor="center",
        font=dict(size=16)
    ),
    coloraxis_colorbar=dict(
        title=dict(text="Índice<br>(/10k hab.)", font=dict(size=11)),
        tickfont=dict(size=10),
        thickness=16,
        len=0.6,
        x=1.0,
        tickvals=[0, vmax_cap * 0.25, vmax_cap * 0.5, vmax_cap * 0.75, vmax_cap],
        ticktext=[
            "0",
            f"{vmax_cap*0.25:.0f}",
            f"{vmax_cap*0.5:.0f} (mediana≈{mediana:.0f})",
            f"{vmax_cap*0.75:.0f}",
            f"≥{vmax_cap:.0f}",
        ],
    ),
    # Anotação de rodapé
    annotations=[dict(
        text=(f"🔴 Baixa intensidade: < {q1:.0f}/10k hab.  "
              f"🟡 Média: {q1:.0f}–{q3:.0f}/10k  "
              f"🟢 Alta: > {q3:.0f}/10k  |  "
              f"{len(mapa)} municípios com cobertura registrada"),
        xref="paper", yref="paper",
        x=0.5, y=-0.02,
        xanchor="center", yanchor="top",
        showarrow=False,
        font=dict(size=10, color="#555"),
    )]
)

caminho = OUTPUT_DIR / "mapa_intensidade_interativo.html"
fig.write_html(
    str(caminho),
    include_plotlyjs="cdn",       # carrega Plotly via CDN — arquivo menor
    full_html=True,
    config={
        "scrollZoom": True,
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["lasso2d","select2d"],
        "toImageButtonOptions": {
            "format": "png",
            "filename": "intensidade_alesc",
            "width": 1400,
            "height": 900,
        }
    }
)
print(f"✓ {caminho.name} — {caminho.stat().st_size / 1024:.0f} KB")python3 map