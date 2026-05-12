# -*- coding: utf-8 -*-
"""
relatorio_mensal_html.py — Relatório mensal da Rádio Alesc em HTML.

Uso:
    cd ~/coding/radio_alesc
    source radio/bin/activate
    python3 relatorio_mensal_html.py
    
# Mês específico (sem menu interativo)
python3 relatorio_mensal_html.py --mes 2025-11
python3 relatorio_mensal_html.py --mes 2026-03

# Com imagem
ython3 relatorio_mensal_html.py --mes 2025-11 --imagem

# Sem argumento: abre o menu e lista os anos/meses disponíveis
python3 relatorio_mensal_html.p

Saída: outputs/relatorio_radio_alesc_<mes>_<ano>.html
Para PDF: abrir no Chrome/Firefox → Ctrl+P → Salvar como PDF → Layout: Paisagem
"""

import pandas as pd
import unicodedata, re, sys, subprocess, platform, argparse
from pathlib import Path
from datetime import datetime
from io import StringIO

try:
    import plotly.express as px
    import plotly.io as pio
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    print("AVISO: plotly não instalado — mapa interativo desativado. pip install plotly")

OUTPUT_DIR   = Path("outputs")
POP_SC_TOTAL = 7_610_361
OUTPUT_DIR.mkdir(exist_ok=True)

MESES_PT = {
    1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril",
    5:"Maio",    6:"Junho",     7:"Julho", 8:"Agosto",
    9:"Setembro",10:"Outubro",  11:"Novembro", 12:"Dezembro"
}

# Centroides de todos os 295 municípios de SC (lat/lon/pop)
CENTROIDES_POP_CSV = """municipio,lat,lon,pop
Abdon Batista,-27.6097,-51.0228,2425
Abelardo Luz,-26.5697,-52.3261,17392
Agrolândia,-27.4058,-49.8236,10260
Agronômica,-27.2728,-49.8583,5131
Água Doce,-26.9944,-51.5531,6975
Águas de Chapecó,-27.1844,-52.9878,6108
Águas Frias,-26.8644,-52.7278,2407
Águas Mornas,-27.7069,-48.8286,5801
Alfredo Wagner,-27.6947,-49.3358,9482
Alto Bela Vista,-27.3722,-52.0047,2150
Anchieta,-26.5328,-53.3378,6188
Angelina,-27.575,-48.9964,5123
Anita Garibaldi,-27.6947,-51.1303,9096
Anitápolis,-27.9056,-49.1278,3292
Antônio Carlos,-27.465,-48.7508,11024
Apiúna,-27.0397,-49.3872,9867
Arabutã,-27.1556,-52.1539,4229
Araquari,-26.3761,-48.7214,40890
Araranguá,-28.9347,-49.4861,71922
Armazém,-28.2547,-49.0128,8834
Arroio Trinta,-26.9281,-51.3428,3547
Arvoredo,-27.0425,-52.2889,1980
Ascurra,-26.9747,-49.3694,9600
Atalanta,-27.3828,-49.7878,3487
Aurora,-27.3097,-49.6378,5617
Balneário Arroio do Silva,-28.9833,-49.4083,12283
Balneário Barra do Sul,-26.4572,-48.6108,13373
Balneário Camboriú,-26.9903,-48.6347,139155
Balneário Gaivota,-29.1167,-49.5833,10547
Balneário Piçarras,-26.7603,-48.6708,27127
Balneário Rincão,-28.8333,-49.25,12081
Bandeirante,-26.5828,-53.5714,2928
Barra Bonita,-26.6033,-53.4944,1896
Barra Velha,-26.6328,-48.6839,45369
Bela Vista do Toldo,-26.0528,-50.4778,6222
Belmonte,-26.5044,-53.4717,2048
Benedito Novo,-26.7833,-49.3728,11618
Biguaçu,-27.4939,-48.6558,70471
Blumenau,-26.9194,-49.0661,361261
Bocaina do Sul,-27.7394,-50.0044,3017
Bom Jardim da Serra,-28.3342,-49.6258,4536
Bom Jesus,-26.7522,-52.3894,2418
Bom Jesus do Oeste,-26.7089,-53.0778,2185
Bom Retiro,-27.7961,-49.4892,9548
Bombinhas,-27.1417,-48.5153,17583
Botuverá,-27.2028,-49.0742,5178
Braço do Norte,-28.2742,-49.1647,33773
Braço do Trombudo,-27.3189,-49.92,4264
Brunópolis,-27.3344,-51.0889,2851
Brusque,-27.099,-48.9167,141385
Caçador,-26.7753,-51.0144,73720
Caibi,-27.0628,-53.2453,6304
Calmon,-26.5344,-51.0378,3779
Camboriú,-27.0228,-48.6558,87179
Campo Alegre,-26.1997,-49.2644,12501
Campo Belo do Sul,-27.8942,-50.7644,7400
Campo Erê,-26.3917,-53.0878,9623
Campos Novos,-27.4025,-51.2253,36932
Canelinha,-27.2694,-48.7747,11823
Canoinhas,-26.1806,-50.39,55016
Capão Alto,-28.0208,-50.5011,3134
Capinzal,-27.3408,-51.6158,23314
Capivari de Baixo,-28.4458,-49.0011,24022
Catanduvas,-27.0728,-51.6578,10566
Caxambu do Sul,-27.1503,-52.8644,5003
Celso Ramos,-27.6286,-51.3017,2768
Cerro Negro,-27.77,-50.87,3407
Chapadão do Lageado,-27.5628,-49.6997,2140
Chapecó,-27.1003,-52.615,254785
Cocal do Sul,-28.6025,-49.3258,16432
Concórdia,-27.2342,-52.0278,81646
Cordilheira Alta,-27.2028,-52.6489,5300
Coronel Freitas,-26.9044,-52.7214,10388
Coronel Martins,-26.5514,-52.6289,2800
Correia Pinto,-27.5858,-50.3608,15447
Corupá,-26.4264,-49.2411,15267
Criciúma,-28.6775,-49.3697,214493
Cunha Porã,-26.8931,-53.1736,10953
Cunhataí,-26.9439,-53.1178,2400
Curitibanos,-27.2825,-50.5831,40045
Descanso,-26.8228,-53.5017,8530
Dionísio Cerqueira,-26.255,-53.6369,15008
Dona Emma,-26.9294,-49.5208,4221
Doutor Pedrinho,-26.7422,-49.4783,3500
Entre Rios,-26.7044,-52.5528,3800
Ermo,-28.9894,-49.6814,2200
Erval Velho,-27.2797,-51.4539,4885
Faxinal dos Guedes,-26.85,-52.2581,11192
Flor do Sertão,-26.7044,-53.4028,1800
Florianópolis,-27.5954,-48.548,537211
Formosa do Sul,-26.6578,-52.8578,2500
Forquilhinha,-28.7453,-49.4728,31431
Fraiburgo,-27.0228,-50.9192,33481
Frei Rogério,-27.1736,-50.8278,3200
Galvão,-26.4339,-52.5578,3900
Garopaba,-28.0239,-48.6228,29959
Garuva,-26.0331,-48.8508,18545
Gaspar,-26.9314,-48.9578,72570
Governador Celso Ramos,-27.3183,-48.5578,13000
Grão Pará,-28.1764,-49.2297,6277
Gravatal,-28.3228,-49.0458,11400
Guabiruba,-27.0636,-48.9836,22500
Guaraciaba,-26.5947,-53.5228,10796
Guaramirim,-26.4728,-48.9978,46757
Guarujá do Sul,-26.3828,-53.5194,5000
Guatambú,-27.1506,-52.7983,5000
Herval d'Oeste,-27.1906,-51.4869,21724
Ibiam,-27.2653,-51.4808,2200
Ibicaré,-27.0819,-51.3517,3200
Ibirama,-27.0572,-49.5178,19862
Içara,-28.7133,-49.3036,58055
Ilhota,-26.8994,-48.8283,13300
Imaruí,-28.3292,-48.8197,11881
Imbituba,-28.2406,-48.6658,52579
Imbuia,-27.4878,-49.5228,5300
Indaial,-26.8978,-49.2333,71549
Iomerê,-27.0022,-51.2428,2800
Ipira,-27.3978,-51.7878,4100
Iporã do Oeste,-26.9978,-53.5325,9335
Ipuaçu,-26.6428,-52.4678,7400
Ipumirim,-27.0714,-52.0928,8000
Iraceminha,-26.8228,-53.2778,4500
Irani,-27.0303,-51.8717,10195
Irati,-26.5344,-52.4678,3800
Irineópolis,-26.2344,-50.7894,10285
Itá,-27.2906,-52.3244,7067
Itaiópolis,-26.3378,-49.9083,22051
Itajaí,-26.9078,-48.6619,264054
Itapema,-27.0861,-48.6147,75940
Itapiranga,-27.1681,-53.7108,16638
Itapoá,-26.1244,-48.6139,24100
Ituporanga,-27.4128,-49.5978,26525
Jaborá,-27.1797,-51.7378,3600
Jacinto Machado,-28.9981,-49.7614,10624
Jaguaruna,-28.6128,-49.0297,20375
Jaraguá do Sul,-26.4853,-49.0689,182660
Jardinópolis,-26.7228,-52.9278,2500
Joaçaba,-27.1742,-51.5044,30146
Joinville,-26.3044,-48.8487,616317
José Boiteux,-27.0028,-49.6478,4800
Jupiá,-26.4144,-52.9028,2400
Lacerdópolis,-27.2497,-51.5544,2100
Lages,-27.8158,-50.3258,164981
Laguna,-28.4808,-48.7811,42785
Lajeado Grande,-26.7678,-52.4878,2300
Laurentino,-27.2233,-49.7378,6500
Lauro Müller,-28.3892,-49.3997,14381
Lebon Régis,-26.9256,-50.6917,11500
Leoberto Leal,-27.6219,-49.1528,3900
Lindóia do Sul,-27.0519,-52.1497,4549
Lontras,-27.1578,-49.5303,12873
Luiz Alves,-26.7158,-48.925,10900
Luzerna,-27.1294,-51.4742,5000
Macieira,-26.7906,-51.3128,2200
Mafra,-26.1097,-49.8019,55286
Major Gercino,-27.4361,-48.9119,3000
Major Vieira,-26.3694,-50.3233,7425
Maracajá,-28.8328,-49.4458,7100
Maravilha,-26.7692,-53.1717,28251
Marema,-26.9044,-52.5878,2300
Massaranduba,-26.6086,-49.0075,16700
Matos Costa,-26.4728,-51.1544,3100
Meleiro,-28.8278,-49.6358,7700
Mirim Doce,-27.1611,-50.0867,2500
Modelo,-26.7819,-53.0239,4080
Mondaí,-27.0975,-53.4044,10066
Monte Carlo,-27.2278,-50.9628,3900
Monte Castelo,-26.4578,-50.2244,8800
Morro da Fumaça,-28.6544,-49.2278,17400
Morro Grande,-28.7667,-49.7,3200
Navegantes,-26.8994,-48.6539,85734
Nova Erechim,-26.9,-52.9097,5155
Nova Itaberaba,-26.9406,-52.8408,4200
Nova Trento,-27.2883,-48.9278,13727
Nova Veneza,-28.6381,-49.5025,14500
Novo Horizonte,-26.4578,-52.81,3400
Orleans,-28.36,-49.2958,23661
Otacílio Costa,-27.4786,-50.1228,18900
Ouro,-27.3544,-51.6178,7200
Ouro Verde,-26.6978,-52.3028,4100
Paial,-27.2478,-52.4378,1900
Painel,-28.0019,-50.1006,2400
Palhoça,-27.6447,-48.6658,178679
Palma Sola,-26.3525,-53.2869,7605
Palmeira,-27.9236,-50.1583,5100
Palmitos,-27.0711,-53.1578,15626
Papanduva,-26.3822,-50.1478,19150
Paraíso,-26.6111,-53.2897,4200
Passo de Torres,-29.3244,-49.7178,7500
Passos Maia,-26.7844,-51.9244,4034
Paulo Lopes,-27.9617,-48.6808,7200
Pedras Grandes,-28.4489,-49.19,4100
Penha,-26.7711,-48.6447,26400
Peritiba,-27.4278,-51.9428,3600
Pescaria Brava,-28.3833,-48.8667,14000
Petrolândia,-27.5317,-49.6878,9800
Pinhalzinho,-26.8472,-52.9869,21972
Pinheiro Preto,-27.0814,-51.2183,3600
Piratuba,-27.4228,-51.7728,4700
Planalto Alegre,-27.0428,-52.7739,3500
Pomerode,-26.7428,-49.1756,34289
Ponte Alta,-27.4869,-50.3814,6000
Ponte Alta do Norte,-27.1542,-50.4553,3200
Ponte Serrada,-26.8694,-52.0158,10649
Porto Belo,-27.1558,-48.5508,27688
Porto União,-26.2331,-51.0794,32970
Pouso Redondo,-27.2578,-49.9478,14600
Praia Grande,-29.1928,-49.9578,7300
Presidente Castello Branco,-27.1778,-51.7244,1800
Presidente Getúlio,-27.0478,-49.6247,20010
Presidente Nereu,-27.2528,-49.7478,2700
Princesa,-26.4539,-53.5494,2500
Quilombo,-26.7306,-52.7244,11022
Rancho Queimado,-27.6828,-49.0119,3000
Rio das Antas,-26.8942,-51.0817,9800
Rio do Campo,-26.9578,-50.1428,5700
Rio do Oeste,-27.1933,-49.7978,7200
Rio do Sul,-27.2147,-49.6436,72587
Rio dos Cedros,-26.7458,-49.2747,10865
Rio Fortuna,-28.1728,-49.1042,4600
Rio Negrinho,-26.2553,-49.5197,39261
Rio Rufino,-27.8786,-49.9,2800
Riqueza,-27.0814,-53.3367,4700
Rodeio,-26.9239,-49.3528,11700
Romelândia,-26.6828,-53.3517,5300
Salete,-26.9828,-49.6878,7200
Saltinho,-26.5847,-52.6553,3200
Salto Veloso,-26.9553,-51.2019,4300
Sangão,-28.5656,-49.1264,12100
Santa Cecília,-26.9594,-50.4247,15546
Santa Helena,-26.9378,-53.6183,2700
Santa Rosa de Lima,-28.0356,-49.1378,2200
Santa Rosa do Sul,-29.1244,-49.7358,8900
Santa Terezinha,-26.7806,-50.0278,8066
Santa Terezinha do Progresso,-26.8236,-53.1978,3300
Santiago do Sul,-26.5678,-52.5278,2200
Santo Amaro da Imperatriz,-27.6836,-48.7906,22800
São Bento do Sul,-26.25,-49.3797,83277
São Bernardino,-26.4528,-52.8778,3100
São Bonifácio,-27.9053,-48.9378,3200
São Carlos,-27.0778,-53.0478,10282
São Cristóvão do Sul,-27.2967,-50.3728,5400
São Domingos,-26.5647,-52.5344,9226
São Francisco do Sul,-26.2433,-48.6397,52674
São João Batista,-27.2728,-48.8483,32687
São João do Itaperiú,-26.6558,-48.7753,5000
São João do Oeste,-27.0903,-53.5581,6400
São João do Sul,-29.2458,-49.8078,7000
São Joaquim,-28.2942,-49.9317,25939
São José,-27.6136,-48.6369,253705
São José do Cedro,-26.47,-53.5528,14167
São José do Cerrito,-27.6528,-50.5817,9000
São Lourenço do Oeste,-26.3578,-52.8478,24791
São Ludgero,-28.3158,-49.1697,13509
São Martinho,-28.1353,-49.1267,3700
São Miguel da Boa Vista,-26.7539,-53.4017,2400
São Miguel do Oeste,-26.7278,-53.5139,44330
São Pedro de Alcântara,-27.5847,-48.8028,5000
Saudades,-26.9353,-53.0028,10265
Schroeder,-26.4153,-49.0681,17900
Seara,-27.1503,-52.3167,18620
Serra Alta,-26.7278,-52.8678,4100
Siderópolis,-28.5981,-49.4258,14300
Sombrio,-29.1058,-49.6333,29991
Sul Brasil,-26.7214,-52.9678,2600
Taió,-27.1144,-49.9994,18310
Tangará,-27.1022,-51.2494,8143
Tigrinhos,-26.7139,-53.2878,2100
Tijucas,-27.2422,-48.6344,51592
Timbé do Sul,-28.9781,-49.8261,5400
Timbó,-26.8228,-49.2717,46099
Timbó Grande,-26.6144,-50.9028,6800
Três Barras,-26.1208,-50.3133,19746
Treviso,-28.5406,-49.4928,3900
Treze de Maio,-28.5658,-49.1856,7200
Treze Tílias,-26.6044,-51.4017,8787
Tubarão,-28.4678,-49.0128,110088
Tunápolis,-26.9828,-53.6178,4916
Turvo,-28.9258,-49.6897,13043
União do Oeste,-26.7928,-52.8378,2900
Urubici,-28.0158,-49.5919,10834
Urupema,-28.0006,-49.8767,2700
Urussanga,-28.52,-49.3228,20919
Vargeão,-26.8339,-52.13,4400
Vargem,-27.5506,-50.86,3300
Vargem Bonita,-26.9878,-52.0008,4400
Vidal Ramos,-27.3897,-49.3578,7000
Videira,-27.0078,-51.1536,55466
Vitor Meireles,-26.8933,-49.7367,5400
Witmarsum,-27.3278,-49.5578,6000
Xanxerê,-26.8758,-52.4031,51607
Xavantina,-27.0617,-52.3478,5500
Xaxim,-26.9606,-52.5369,31918
Zortéa,-27.4722,-51.5531,3930
"""

# ── normalização ──────────────────────────────────────────────────────────────
def normalizar(t):
    if pd.isna(t): return ""
    t = str(t).lower().strip().replace("-"," ").replace("'"," ")
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn")

def normalizar_radio(t):
    if pd.isna(t): return ""
    t = str(t).lower().strip()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", t)

def fmt_n(n):  return f"{int(n):,}".replace(",",".")
def fmt_pop(n):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000:     return f"{n/1_000:.0f}K"
    return str(int(n))

# ── carrega dados ─────────────────────────────────────────────────────────────
def carregar():
    print("Carregando dados...")
    df = pd.read_csv("outputs/dataset_consolidado.csv", encoding="utf-8-sig", low_memory=False)
    df["Radio_norm"]  = df["Radio"].apply(normalizar_radio)
    df["Cidade_norm"] = df["Cidade"].apply(normalizar)
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce", format="mixed")
    df = df.dropna(subset=["Data"])
    df["Ano"] = df["Data"].dt.year.astype(int)
    df["Mes"] = df["Data"].dt.month.astype(int)
    return df

def carregar_abr():
    mapa = {}
    for nome in ["data/radios_municipios_-_mar2026.csv","data/radios municipios - mar2026.csv"]:
        if Path(nome).exists():
            raw = pd.read_csv(nome, encoding="utf-8", sep=None, engine="python", header=None)
            for _, row in raw.iterrows():
                rr = str(row.iloc[0]).strip()
                if not rr or rr=="nan": continue
                rn = normalizar_radio(rr)
                cids = [normalizar(str(v).split("/")[0].strip()) for v in row.iloc[1:]
                        if pd.notna(v) and str(v).strip() not in ("nan","")]
                if cids: mapa[rn] = set(cids)
            break
    return mapa

def _carregar_centroides():
    """Retorna dict: cidade_norm -> {municipio, lat, lon, pop}"""
    df = pd.read_csv(StringIO(CENTROIDES_POP_CSV))
    df["Cidade_norm"] = df["municipio"].apply(normalizar)
    return df.set_index("Cidade_norm").to_dict("index")

# ── métricas ──────────────────────────────────────────────────────────────────
def calcular(df, mapa_abr, ano, mes):
    dfm = df[(df["Ano"]==ano)&(df["Mes"]==mes)].copy()
    if dfm.empty: return None

    df_pop = (df[["Cidade_norm","Populacao"]].dropna()
              .drop_duplicates("Cidade_norm").set_index("Cidade_norm")["Populacao"].to_dict())
    mapa_sede = df.groupby("Radio_norm")["Cidade_norm"].first().to_dict()

    munis = set()
    for rn in dfm["Radio_norm"].dropna().unique():
        if rn in mapa_abr: munis.update(mapa_abr[rn])
        else:
            s = mapa_sede.get(rn,"")
            if s: munis.add(s)
    munis.update(m for m in dfm["Cidade_norm"].dropna().unique() if m)
    munis -= {""}

    pop = sum(df_pop.get(m,0) for m in munis)

    # mês anterior
    ma, ya = (mes-1,ano) if mes>1 else (12,ano-1)
    da = df[(df["Ano"]==ya)&(df["Mes"]==ma)]
    delta = ((len(dfm)-len(da))/max(len(da),1))*100

    # top conteúdos — por população alcançada
    top_cont = []
    for nome, g in dfm.groupby("Comercial"):
        rs = g["Radio_norm"].dropna().unique()
        ms2 = set()
        for rn in rs:
            if rn in mapa_abr: ms2.update(mapa_abr[rn])
            else:
                s = mapa_sede.get(rn,"")
                if s: ms2.add(s)
        ms2.update(m for m in g["Cidade_norm"].dropna().unique() if m)
        p = sum(df_pop.get(m,0) for m in ms2)
        if p>0: top_cont.append({"nome":nome,"pop":p,"veic":len(g),"emissoras":len(rs)})
    top_cont = sorted(top_cont, key=lambda x:-x["pop"])[:10]

    # top cidades (veiculação direta)
    top_cid = (dfm.groupby("Cidade").size().reset_index(name="v")
               .sort_values("v",ascending=False).head(10))

    # top rádios (com cidade-sede)
    mapa_sede_display = df.groupby("Radio_norm")["Cidade"].first().to_dict()
    top_rad = (dfm.groupby("Radio").size().reset_index(name="v")
               .sort_values("v",ascending=False).head(10))
    top_rad["Radio_norm_tmp"] = top_rad["Radio"].apply(normalizar_radio)
    top_rad["Cidade_sede"] = top_rad["Radio_norm_tmp"].map(mapa_sede_display).fillna("")
    top_rad = top_rad.drop(columns=["Radio_norm_tmp"])

    # cobertura por mesorregião — lista completa de municípios (IBGE)
    # Mesorregiões IBGE oficiais (6 mesorregiões, 295 municípios de SC)
    _MESO_MUNIS = {
        "Oeste Catarinense": {
            "abelardo luz", "agua doce", "aguas de chapeco", "aguas frias",
            "alto bela vista", "anchieta", "arabuta", "arroio trinta",
            "arvoredo", "bandeirante", "barra bonita", "belmonte",
            "bom jesus", "bom jesus do oeste", "cacador", "caibi",
            "calmon", "campo ere", "capinzal", "catanduvas",
            "caxambu do sul", "chapeco", "concordia", "cordilheira alta",
            "coronel freitas", "coronel martins", "cunha pora", "cunhatai",
            "descanso", "dionisio cerqueira", "entre rios", "erval velho",
            "faxinal dos guedes", "flor do sertao", "formosa do sul", "fraiburgo",
            "galvao", "guaraciaba", "guaruja do sul", "guatambu",
            "herval d oeste", "ibiam", "ibicare", "iomere",
            "ipira", "ipora do oeste", "ipuacu", "ipumirim",
            "iraceminha", "irani", "irati", "ita",
            "itapiranga", "jabora", "jardinopolis", "joacaba",
            "jupia", "lacerdopolis", "lajeado grande", "lebon regis",
            "lindoia do sul", "luzerna", "macieira", "maravilha",
            "marema", "matos costa", "modelo", "mondai",
            "nova erechim", "nova itaberaba", "novo horizonte", "ouro",
            "ouro verde", "paial", "palma sola", "palmitos",
            "paraiso", "passos maia", "peritiba", "pinhalzinho",
            "pinheiro preto", "piratuba", "planalto alegre", "ponte serrada",
            "presidente castello branco", "princesa", "quilombo", "rio das antas",
            "riqueza", "romelandia", "saltinho", "salto veloso",
            "santa helena", "santa terezinha do progresso", "santiago do sul", "sao bernardino",
            "sao carlos", "sao domingos", "sao joao do oeste", "sao jose do cedro",
            "sao lourenco do oeste", "sao miguel da boa vista", "sao miguel do oeste", "saudades",
            "seara", "serra alta", "sul brasil", "tangara",
            "tigrinhos", "treze tilias", "tunapolis", "uniao do oeste",
            "vargeao", "vargem bonita", "videira", "xanxere",
            "xavantina", "xaxim",
        },
        "Norte Catarinense": {
            "araquari", "balneario barra do sul", "bela vista do toldo", "campo alegre",
            "canoinhas", "corupa", "garuva", "guaramirim",
            "irineopolis", "itaiopolis", "itapoa", "jaragua do sul",
            "joinville", "mafra", "major vieira", "massaranduba",
            "monte castelo", "papanduva", "porto uniao", "rio negrinho",
            "santa terezinha", "sao bento do sul", "sao francisco do sul", "schroeder",
            "timbo grande", "tres barras",
        },
        "Serrana": {
            "abdon batista", "anita garibaldi", "bocaina do sul", "bom jardim da serra",
            "bom retiro", "brunopolis", "campo belo do sul", "campos novos",
            "capao alto", "celso ramos", "cerro negro", "correia pinto",
            "curitibanos", "frei rogerio", "lages", "monte carlo",
            "otacilio costa", "painel", "palmeira", "ponte alta",
            "ponte alta do norte", "rio rufino", "santa cecilia", "sao cristovao do sul",
            "sao joaquim", "sao jose do cerrito", "urubici", "urupema",
            "vargem", "zortea",
        },
        "Vale do Itajaí": {
            "agrolandia", "agronomica", "apiuna", "ascurra",
            "atalanta", "aurora", "balneario camboriu", "balneario picarras",
            "barra velha", "benedito novo", "blumenau", "bombinhas",
            "botuvera", "braco do trombudo", "brusque", "camboriu",
            "chapadao do lageado", "dona emma", "doutor pedrinho", "gaspar",
            "guabiruba", "ibirama", "ilhota", "imbuia",
            "indaial", "itajai", "itapema", "ituporanga",
            "jose boiteux", "laurentino", "lontras", "luiz alves",
            "mirim doce", "navegantes", "penha", "petrolandia",
            "pomerode", "porto belo", "pouso redondo", "presidente getulio",
            "presidente nereu", "rio do campo", "rio do oeste", "rio do sul",
            "rio dos cedros", "rodeio", "salete", "sao joao do itaperiu",
            "taio", "timbo", "trombudo central", "vidal ramos",
            "vitor meireles", "witmarsum",
        },
        "Grande Florianópolis": {
            "aguas mornas", "alfredo wagner", "angelina", "anitapolis",
            "antonio carlos", "biguacu", "canelinha", "florianopolis",
            "governador celso ramos", "leoberto leal", "major gercino", "nova trento",
            "palhoca", "paulo lopes", "rancho queimado", "santo amaro da imperatriz",
            "sao bonifacio", "sao joao batista", "sao jose", "sao pedro de alcantara",
            "tijucas",
        },
        "Sul Catarinense": {
            "ararangua", "armazem", "balneario arroio do silva", "balneario gaivota",
            "balneario rincao", "braco do norte", "capivari de baixo", "cocal do sul",
            "criciuma", "ermo", "forquilhinha", "garopaba",
            "grao para", "gravatal", "icara", "imarui",
            "imbituba", "jacinto machado", "jaguaruna", "laguna",
            "lauro muller", "maracaja", "meleiro", "morro da fumaca",
            "morro grande", "nova veneza", "orleans", "passo de torres",
            "pedras grandes", "pescaria brava", "praia grande", "rio fortuna",
            "sangao", "santa rosa de lima", "santa rosa do sul", "sao joao do sul",
            "sao ludgero", "sao martinho", "sideropolis", "sombrio",
            "timbe do sul", "treviso", "treze de maio", "tubarao",
            "turvo", "urussanga",
        },
    }
    cob_meso = {}
    for nome_m, muni_set in _MESO_MUNIS.items():
        # municípios da mesorregião que foram alcançados (sinal ou veiculação)
        alcancados = munis & muni_set
        # veiculações diretas em qualquer município da mesorregião
        veics = int(dfm["Cidade_norm"].isin(muni_set).sum())
        cob_meso[nome_m] = {
            "veiculacoes": veics,
            "munis_alcancados": len(alcancados),
            "munis_total": len(muni_set),
        }

    # ── NOVAS MÉTRICAS ────────────────────────────────────────────
    dias_mes  = pd.Timestamp(ano, mes, 1).days_in_month
    media_diaria = len(dfm) / dias_mes

    total_ano = len(df[(df["Ano"]==ano) & (df["Mes"]<=mes)])

    hora_pico = None
    if "Hora_int" in dfm.columns:
        horas = dfm["Hora_int"].dropna()
        if not horas.empty:
            hora_pico = int(horas.mode().iloc[0])

    audiencia_total = 0
    if "Audiencia_Abrangencia" in dfm.columns:
        audiencia_total = dfm["Audiencia_Abrangencia"].fillna(0).sum()

    # Distribuição por tipo de conteúdo
    tipo_veic = {}
    if "Tipo" in dfm.columns:
        tipo_veic = dfm["Tipo"].fillna("Sem tipo").value_counts().head(4).to_dict()

    # Municípios alcançados (diretos, pelo sinal)
    diretos = set(dfm["Cidade_norm"].dropna().unique()) - {""}

    return {
        "ano":ano,"mes":mes,
        "total_veic":    len(dfm),
        "total_emiss":   dfm["Radio_norm"].nunique(),
        "total_munis":   len(munis),
        "pop":           pop,
        "pct_sc":        pop/POP_SC_TOTAL*100,
        "delta":         delta,
        "top_cont":      top_cont,
        "top_cid":       top_cid.to_dict("records"),
        "top_rad":       top_rad.to_dict("records"),
        "cob_meso":      cob_meso,
        # novas
        "media_diaria":   media_diaria,
        "total_ano":      total_ano,
        "hora_pico":      hora_pico,
        "audiencia_total": audiencia_total,
        "tipo_veic":      tipo_veic,
        "munis_set":      munis,
        "diretos_set":    diretos,
        "mapa_sede":      mapa_sede,
        "veic_por_muni":  dfm["Cidade_norm"].value_counts().to_dict(),
    }

# ── Mapa Plotly dos municípios alcançados no mês ──────────────────────────────
def gerar_mapa_mensal_div(dfm, m, cent_dict):
    """Gera div Plotly scatter_mapbox com cobertura municipal do mês."""
    if not HAS_PLOTLY:
        return ""

    munis    = m["munis_set"]
    diretos  = m["diretos_set"]

    # contagem de veiculações diretas por município
    veic_por_muni = dfm["Cidade_norm"].value_counts().to_dict()

    rows = []
    for cn in munis:
        if cn not in cent_dict:
            continue
        c = cent_dict[cn]
        n_veic = veic_por_muni.get(cn, 0)
        tipo = "Veiculação direta" if cn in diretos else "Sinal da emissora"
        rows.append({
            "municipio": c["municipio"],
            "lat":       c["lat"],
            "lon":       c["lon"],
            "pop":       c.get("pop", 0),
            "veiculacoes": n_veic,
            "tipo":      tipo,
        })

    if not rows:
        return ""

    df_map = pd.DataFrame(rows)
    cores = {"Veiculação direta": "#1a5fa8", "Sinal da emissora": "#7ab3e0"}

    fig = px.scatter_map(
        df_map, lat="lat", lon="lon",
        size="pop", color="tipo",
        color_discrete_map=cores,
        hover_name="municipio",
        hover_data={"lat": False, "lon": False, "pop": True,
                    "veiculacoes": True, "tipo": True},
        size_max=42, zoom=6.4,
        center={"lat": -27.5, "lon": -50.8},
        map_style="carto-positron",
        labels={"tipo": "Cobertura", "pop": "População", "veiculacoes": "Veiculações diretas"},
        category_orders={"tipo": ["Veiculação direta", "Sinal da emissora"]},
    )
    fig.update_layout(
        autosize=True,
        height=520,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            x=0.01, y=0.99,
            bgcolor="rgba(255,255,255,0.88)",
            bordercolor="#b8cde0", borderwidth=1,
            font=dict(size=10),
            title_text="",
        ),
        paper_bgcolor="#eef4fb",
    )

    return pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs=False,
        config={"displayModeBar": False, "scrollZoom": True},
    )

# ── Mapa SVG estático (funciona em PDF) ──────────────────────────────────────
def gerar_mapa_svg(m, cent_dict):
    """SVG com todos os 295 municípios em coordenadas geográficas reais."""
    import math
    SVG_W, SVG_H = 580, 400

    LON_MIN, LON_MAX = -53.85, -48.35
    LAT_MAX, LAT_MIN = -25.90, -29.45   # invertido: lat crescente = y decrescente

    def to_xy(lat, lon):
        x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * SVG_W
        y = (lat - LAT_MAX) / (LAT_MIN - LAT_MAX) * SVG_H
        return round(x, 1), round(y, 1)

    munis        = m["munis_set"]
    diretos      = m["diretos_set"]
    veic_por_muni= m["veic_por_muni"]

    # max_pop para escala de raios (sqrt)
    pops = [c.get("pop", 0) for c in cent_dict.values() if c.get("pop", 0) > 0]
    max_pop = max(pops) if pops else 1

    circles = []
    for cn, c in cent_dict.items():
        lat, lon = c["lat"], c["lon"]
        pop = c.get("pop", 0)
        r = max(2.5, min(15, math.sqrt(pop / max_pop) * 18))
        x, y = to_xy(lat, lon)

        if cn in diretos:
            n_veic = veic_por_muni.get(cn, 0)
            if n_veic >= 10:
                color, opac, stroke = "#0d3d6e", 0.90, "#ffffff"
            elif n_veic >= 3:
                color, opac, stroke = "#1a5fa8", 0.85, "#ffffff"
            else:
                color, opac, stroke = "#4a90d9", 0.80, "#ffffff"
        elif cn in munis:
            color, opac, stroke = "#7ab3e0", 0.70, "#c5dff0"
        else:
            color, opac, stroke = "#cdd8e5", 0.35, "#b8c8d8"

        circles.append((r, cn, x, y, color, opac, stroke, pop, c["municipio"]))

    # renderiza maiores primeiro (ficam embaixo)
    circles.sort(key=lambda c: -c[0])

    svg_parts = []
    for r, cn, x, y, color, opac, stroke, pop, nome in circles:
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" '
            f'fill="{color}" opacity="{opac}" stroke="{stroke}" stroke-width="0.5">'
            f'<title>{nome} — {fmt_pop(pop)}</title>'
            f'</circle>'
        )
        if pop > 120_000:
            svg_parts.append(
                f'<text x="{x}" y="{y + r + 7}" text-anchor="middle" '
                f'font-size="6.5" fill="#1c2b3a" font-family="sans-serif" '
                f'opacity="0.85">{nome}</text>'
            )

    LY = SVG_H + 12
    legenda = (
        f'<circle cx="10" cy="{LY}" r="5" fill="#1a5fa8" opacity="0.85"/>'
        f'<text x="19" y="{LY+4}" font-size="8.5" fill="#5a6a7e" font-family="sans-serif">Veiculação direta</text>'
        f'<circle cx="120" cy="{LY}" r="5" fill="#7ab3e0" opacity="0.70"/>'
        f'<text x="129" y="{LY+4}" font-size="8.5" fill="#5a6a7e" font-family="sans-serif">Sinal da emissora</text>'
        f'<circle cx="232" cy="{LY}" r="5" fill="#cdd8e5" opacity="0.35"/>'
        f'<text x="241" y="{LY+4}" font-size="8.5" fill="#5a6a7e" font-family="sans-serif">Sem cobertura</text>'
        f'<text x="{SVG_W}" y="{LY+4}" text-anchor="end" font-size="7.5" fill="#8a9bb0" font-family="sans-serif">Tamanho = população</text>'
    )

    return (
        f'<svg viewBox="0 0 {SVG_W} {SVG_H + 24}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;height:auto;background:#eef4fb;border-radius:6px;display:block">'
        f'{"".join(svg_parts)}'
        f'{legenda}'
        f'</svg>'
    )

# ── Helpers HTML ──────────────────────────────────────────────────────────────
def _meso_html(cob_meso):
    partes = []
    max_v = max((info["veiculacoes"] for info in cob_meso.values()), default=1) or 1
    for nm, info in cob_meso.items():
        v   = info["veiculacoes"]
        alc = info.get("munis_alcancados", 0)
        tot = info.get("munis_total", 0)
        pct = v / max_v * 100
        cls = "meso-item ativo" if v > 0 else "meso-item"
        muni_str = f"{alc}/{tot} munic." if tot else ""
        partes.append(
            f'<div class="{cls}">'
            f'<div class="meso-nome">{nm}'
            f'<span class="meso-muni-badge">{muni_str}</span></div>'
            f'<div class="meso-bar-row">'
            f'<div class="meso-bar-wrap"><div class="meso-bar" style="width:{pct:.0f}%"></div></div>'
            f'<span class="meso-veic">{fmt_n(v)}</span>'
            f'</div>'
            f'</div>'
        )
    return "".join(partes)

def _tipo_html(tipo_veic):
    if not tipo_veic:
        return '<p style="color:#8a9bb0;font-size:11px">Sem dados de tipo</p>'
    total = sum(tipo_veic.values())
    mx = max(tipo_veic.values())
    rows = ""
    for tipo, cnt in tipo_veic.items():
        pct_bar = cnt/mx*100
        pct_txt = cnt/total*100
        nome_s  = tipo[:35]+"…" if len(tipo)>35 else tipo
        rows += (
            f'<div class="tipo-row">'
            f'<span class="tipo-nome">{nome_s}</span>'
            f'<div class="tipo-bar-wrap"><div class="tipo-bar" style="width:{pct_bar:.0f}%"></div></div>'
            f'<span class="tipo-pct">{pct_txt:.0f}%</span>'
            f'</div>'
        )
    return rows

# ── Geração do HTML ───────────────────────────────────────────────────────────
def gerar_html(m, cent_dict=None, mapa_div=""):
    nome_mes  = MESES_PT[m["mes"]]
    dias_mes  = pd.Timestamp(m["ano"], m["mes"], 1).days_in_month
    periodo   = f"1 a {dias_mes} de {nome_mes} de {m['ano']}"
    gerado_em = datetime.now().strftime("%d/%m/%Y às %H:%M")
    delta_sig = "▲" if m["delta"]>=0 else "▼"
    delta_cls = "positivo" if m["delta"]>=0 else "negativo"

    hora_fmt = f"{m['hora_pico']:02d}h" if m["hora_pico"] is not None else "—"

    # barras
    max_pop_cont = m["top_cont"][0]["pop"] if m["top_cont"] else 1
    max_cid = m["top_cid"][0]["v"]   if m["top_cid"] else 1
    max_rad = m["top_rad"][0]["v"]   if m["top_rad"] else 1

    rows_cont = ""
    for i, c in enumerate(m["top_cont"], 1):
        pct = c["pop"]/max_pop_cont*100
        nome_short = c["nome"][:55]+"…" if len(c["nome"])>55 else c["nome"]
        rows_cont += (
            f'<div class="rank-row">'
            f'<span class="rank-pos">{i:02d}</span>'
            f'<div class="rank-info"><span class="rank-nome">{nome_short}</span>'
            f'<div class="rank-bar-wrap"><div class="rank-bar" style="width:{pct:.1f}%"></div></div></div>'
            f'<div class="rank-stats"><span class="rank-pop">{fmt_pop(c["pop"])}</span>'
            f'<span class="rank-sub">{fmt_n(c["veic"])} veic.</span></div>'
            f'</div>'
        )

    rows_cid = ""
    for i, c in enumerate(m["top_cid"], 1):
        pct = c["v"]/max_cid*100
        rows_cid += (
            f'<div class="rank-row rank-row-sm">'
            f'<span class="rank-pos rank-pos-sm">{i:02d}</span>'
            f'<div class="rank-info"><span class="rank-nome rank-nome-sm">{c["Cidade"]}</span>'
            f'<div class="rank-bar-wrap"><div class="rank-bar rank-bar-verde" style="width:{pct:.1f}%"></div></div></div>'
            f'<span class="rank-val-sm">{fmt_n(c["v"])}</span>'
            f'</div>'
        )

    rows_rad = ""
    for i, r in enumerate(m["top_rad"], 1):
        pct = r["v"]/max_rad*100
        cidade_r = r.get("Cidade_sede", "")
        cidade_tag = f'<span class="rank-cidade-r">{cidade_r}</span>' if cidade_r else ""
        rows_rad += (
            f'<div class="rank-row rank-row-sm">'
            f'<span class="rank-pos rank-pos-sm">{i:02d}</span>'
            f'<div class="rank-info">'
            f'<div class="rank-nome-row">'
            f'{cidade_tag}'
            f'<span class="rank-nome rank-nome-sm">{r["Radio"]}</span>'
            f'</div>'
            f'<div class="rank-bar-wrap"><div class="rank-bar rank-bar-escuro" style="width:{pct:.1f}%"></div></div>'
            f'</div>'
            f'<span class="rank-val-sm">{fmt_n(r["v"])}</span>'
            f'</div>'
        )

    # Mapa SVG estático (PDF-compatível, coordenadas reais)
    mapa_svg = gerar_mapa_svg(m, cent_dict) if cent_dict else _mapa_svg_fallback(m)

    # Dual-mode: Plotly para tela, SVG para impressão
    if mapa_div:
        mapa_content = (
            f'<div class="mapa-screen">{mapa_div}</div>'
            f'<div class="mapa-print">{mapa_svg}</div>'
        )
    else:
        mapa_content = mapa_svg

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório Rádio Alesc — {nome_mes} {m['ano']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --azul:        #1a5fa8;
    --azul-escuro: #0d3d6e;
    --azul-claro:  #e8f0fb;
    --azul-med:    #c5d8f0;
    --verde:       #1e8a4a;
    --dourado:     #c8991a;
    --cinza:       #f4f6f9;
    --borda:       #c2d0e2;
    --texto:       #1c2b3a;
    --texto-leve:  #5a6a7e;
    --branco:      #ffffff;
    --fonte:       'Barlow', sans-serif;
    --fonte-cond:  'Barlow Condensed', sans-serif;
    --sombra:      0 2px 12px rgba(13,61,110,.10);
    --sombra-card: 0 1px 4px rgba(13,61,110,.08), 0 4px 16px rgba(13,61,110,.06);
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: var(--fonte);
    background: #dce6f2;
    color: var(--texto);
    font-size: 15px;
    line-height: 1.5;
  }}

  /* ── PÁGINA ─────────────────────────────────────────── */
  .pagina {{
    max-width: 1120px;
    margin: 0 auto;
    background: #f0f4fa;
    box-shadow: 0 8px 40px rgba(0,0,0,.18);
    border: 1.5px solid var(--borda);
    border-radius: 4px;
  }}

  /* ── CABEÇALHO ─────────────────────────────────────── */
  .cabecalho {{
    background: linear-gradient(135deg, var(--azul-escuro) 0%, var(--azul) 100%);
    display: flex;
    align-items: stretch;
    min-height: 90px;
    position: relative;
    overflow: hidden;
    border-bottom: 3px solid var(--dourado);
  }}
  .cabecalho::before {{
    content:'';
    position:absolute; inset:0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }}
  .cabecalho-logo {{
    padding: 18px 24px;
    display:flex; align-items:center; gap:14px;
    border-right: 1px solid rgba(255,255,255,.15);
    min-width: 210px;
    position: relative; z-index:1;
  }}
  .logo-img {{ height: 50px; filter: brightness(0) invert(1); }}
  .logo-fallback {{ display:flex; flex-direction:column; gap:2px; }}
  .logo-nome {{
    font-family: var(--fonte-cond); font-size:24px; font-weight:700;
    color:white; letter-spacing:.5px; line-height:1;
  }}
  .logo-sub {{ font-size:9px; color:rgba(255,255,255,.65); letter-spacing:1.5px; text-transform:uppercase; }}
  .cabecalho-titulo {{
    flex:1; padding:18px 24px;
    display:flex; flex-direction:column; justify-content:center;
    position: relative; z-index:1;
  }}
  .titulo-rel {{
    font-family:var(--fonte-cond); font-size:11px; font-weight:600;
    color:rgba(255,255,255,.55); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:4px;
  }}
  .titulo-mes {{
    font-family:var(--fonte-cond); font-size:34px; font-weight:700;
    color:white; line-height:1; letter-spacing:.5px;
  }}
  .titulo-periodo {{ font-size:11px; color:rgba(255,255,255,.5); margin-top:4px; }}
  .cabecalho-radio {{
    padding:18px 24px;
    display:flex; flex-direction:column; justify-content:center; align-items:flex-end;
    border-left:1px solid rgba(255,255,255,.15);
    min-width:175px; position:relative; z-index:1;
  }}
  .radio-badge {{
    background:rgba(255,255,255,.10);
    border:1px solid rgba(255,255,255,.22);
    border-radius:8px; padding:10px 18px; text-align:center;
  }}
  .radio-badge-nome {{
    font-family:var(--fonte-cond); font-size:17px; font-weight:700;
    color:white; letter-spacing:.5px;
  }}
  .radio-badge-sub {{ font-size:9px; color:rgba(255,255,255,.5); letter-spacing:1px; text-transform:uppercase; }}

  /* ── FAIXA INFO ─────────────────────────────────────── */
  .faixa-info {{
    background: var(--azul-claro);
    padding: 7px 24px;
    display: flex; gap:28px; align-items:center;
    border-bottom: 1px solid var(--borda);
  }}
  .faixa-item {{ font-size:11px; color:var(--texto-leve); }}
  .faixa-item strong {{ color:var(--azul); font-weight:600; }}

  /* ── CARDS PRINCIPAIS ───────────────────────────────── */
  .cards-wrap {{
    padding: 20px 24px 0;
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 14px;
  }}
  .card {{
    background: var(--branco);
    border: 1.5px solid var(--borda);
    border-radius: 10px;
    padding: 16px 18px 14px;
    position: relative; overflow: hidden;
    box-shadow: var(--sombra-card);
  }}
  .card::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
  }}
  .card-azul::before  {{ background: linear-gradient(90deg, var(--azul-escuro), var(--azul)); }}
  .card-verde::before {{ background: linear-gradient(90deg, #15703c, var(--verde)); }}
  .card-cinza::before {{ background: linear-gradient(90deg, #4a6070, #8a9bb0); }}
  .card-dourado::before {{ background: linear-gradient(90deg, #a07810, var(--dourado)); }}
  .card-label {{
    font-size:10px; font-weight:600; color:var(--texto-leve);
    letter-spacing:1.2px; text-transform:uppercase; margin-bottom:8px;
  }}
  .card-valor {{
    font-family:var(--fonte-cond); font-size:44px; font-weight:700;
    color:var(--azul-escuro); line-height:1; margin-bottom:5px;
  }}
  .card-valor.verde {{ color:var(--verde); }}
  .card-sub {{ font-size:11px; color:var(--texto-leve); }}
  .delta {{
    display:inline-block; font-size:11px; font-weight:600;
    padding:2px 7px; border-radius:20px; margin-top:4px;
  }}
  .positivo {{ background:#e6f7ee; color:#1e8a4a; }}
  .negativo {{ background:#fde8e8; color:#c0392b; }}

  /* ── CARDS SECUNDÁRIOS ──────────────────────────────── */
  .cards-wrap-2 {{
    padding: 14px 24px 0;
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 14px;
  }}
  .card-sm {{
    background: var(--branco);
    border: 1.5px solid var(--borda);
    border-radius: 8px;
    padding: 12px 16px;
    box-shadow: var(--sombra-card);
    display: flex; align-items: center; gap: 14px;
  }}
  .card-sm-icon {{
    width: 36px; height: 36px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
  }}
  .icon-azul    {{ background: var(--azul-claro); }}
  .icon-verde   {{ background: #e6f7ee; }}
  .icon-dourado {{ background: #fef6e4; }}
  .icon-cinza   {{ background: #f0f3f8; }}
  .card-sm-body {{ flex:1; min-width:0; }}
  .card-sm-label {{ font-size:9px; font-weight:600; color:var(--texto-leve); letter-spacing:1.2px; text-transform:uppercase; }}
  .card-sm-valor {{
    font-family:var(--fonte-cond); font-size:24px; font-weight:700;
    color:var(--azul-escuro); line-height:1.1; margin:2px 0 1px;
  }}
  .card-sm-sub {{ font-size:10px; color:var(--texto-leve); }}

  /* ── RANKINGS GRID (pág. 1) ─────────────────────────── */
  .rankings-grid {{
    padding: 16px 24px 20px;
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr;
    gap: 16px;
  }}
  /* ── PÁG. 2: mapa + meso (largura total) ────────────── */
  .pag2 {{
    padding: 20px 24px 0;
  }}

  /* ── SEÇÕES ─────────────────────────────────────────── */
  .secao {{
    background: var(--branco);
    border: 1.5px solid var(--borda);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: var(--sombra-card);
  }}
  .secao-header {{
    padding:12px 18px;
    border-bottom: 1.5px solid var(--borda);
    display:flex; justify-content:space-between; align-items:center;
    background: #fafcff;
  }}
  .secao-titulo {{
    font-family:var(--fonte-cond); font-size:14px; font-weight:700;
    color:var(--azul-escuro); letter-spacing:.5px; text-transform:uppercase;
  }}
  .secao-badge {{
    font-size:9px; font-weight:600; background:var(--azul-claro);
    color:var(--azul); padding:2px 8px; border-radius:20px;
    border: 1px solid var(--azul-med);
  }}
  .secao-body {{ padding:14px 18px; }}

  /* ── SPARKLINE ──────────────────────────────────────── */
  .spark-svg {{ width:100%; overflow:visible; }}
  .spark-label {{ font-size:9px; fill:var(--texto-leve); text-anchor:middle; }}
  .spark-line  {{ fill:none; stroke:var(--azul); stroke-width:2; }}
  .spark-fill  {{ fill:url(#sparkGrad); opacity:.25; }}
  .spark-dot   {{ fill:var(--azul); }}

  /* ── RANKING ────────────────────────────────────────── */
  .rank-row {{
    display:flex; align-items:center; gap:10px;
    padding:7px 0; border-bottom:1px solid #eef1f8;
  }}
  .rank-row:last-child {{ border-bottom:none; }}
  .rank-pos {{
    font-family:var(--fonte-cond); font-size:20px; font-weight:700;
    color:var(--borda); min-width:28px; text-align:right; line-height:1;
  }}
  .rank-row:nth-child(1) .rank-pos {{ color:var(--azul); }}
  .rank-row:nth-child(2) .rank-pos {{ color:#3a7fcc; }}
  .rank-row:nth-child(3) .rank-pos {{ color:#6aaad9; }}
  .rank-info {{ flex:1; min-width:0; }}
  .rank-nome {{
    font-size:13px; font-weight:500; color:var(--texto);
    display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:5px;
  }}
  .rank-bar-wrap {{ height:4px; background:#eef1f6; border-radius:2px; overflow:hidden; }}
  .rank-bar {{ height:100%; background:var(--azul); border-radius:2px; }}
  .rank-bar-verde  {{ background:var(--verde); }}
  .rank-bar-escuro {{ background:var(--azul-escuro); }}
  .rank-stats  {{ text-align:right; min-width:64px; }}
  .rank-pop    {{ font-family:var(--fonte-cond); font-size:15px; font-weight:700; color:var(--azul-escuro); display:block; }}
  .rank-sub    {{ font-size:10px; color:var(--texto-leve); }}
  .rank-row-sm  {{ padding:5px 0; }}
  .rank-pos-sm  {{ font-family:var(--fonte-cond); font-size:14px; font-weight:700; color:var(--borda); min-width:22px; }}
  .rank-row-sm:nth-child(1) .rank-pos-sm {{ color:var(--azul); }}
  .rank-row-sm:nth-child(2) .rank-pos-sm {{ color:#3a7fcc; }}
  .rank-row-sm:nth-child(3) .rank-pos-sm {{ color:#6aaad9; }}
  .rank-nome-sm {{
    font-size:13px; font-weight:500; color:var(--texto);
    display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:3px;
  }}
  .rank-val-sm {{ font-family:var(--fonte-cond); font-size:14px; font-weight:700; color:var(--azul-escuro); min-width:38px; text-align:right; }}

  /* ── MAPA ───────────────────────────────────────────── */
  .mapa-container {{
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--borda);
    margin-bottom: 12px;
    background: #eef4fb;
  }}
  .mapa-print {{ display: none; }}

  /* ── MESORREGIÕES ───────────────────────────────────── */
  .meso-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }}
  .meso-item {{
    background:var(--cinza); border-radius:6px; padding:8px 12px;
    border: 1px solid #dde5f0;
    border-left: 3px solid #c0cfe0;
  }}
  .meso-item.ativo {{ border-left-color:var(--azul); background:#f0f6ff; }}
  .meso-nome {{ font-size:11px; font-weight:600; color:var(--texto); margin-bottom:5px; display:flex; justify-content:space-between; align-items:center; }}
  .meso-muni-badge {{ font-size:9px; font-weight:500; color:var(--texto-leve); background:var(--azul-med); border-radius:10px; padding:1px 7px; }}
  .meso-bar-row {{ display:flex; align-items:center; gap:8px; }}
  .meso-bar-wrap {{ flex:1; height:5px; background:#dde5f0; border-radius:3px; overflow:hidden; }}
  .meso-bar {{ height:100%; background:var(--azul); border-radius:3px; }}
  .meso-veic {{ font-family:var(--fonte-cond); font-size:14px; font-weight:700; color:var(--azul-escuro); min-width:30px; text-align:right; }}

  /* ── CIDADE-SEDE DA RÁDIO ───────────────────────────── */
  .rank-nome-row {{
    display:flex; flex-direction:column; align-items:flex-start; gap:2px; min-width:0; margin-bottom:3px;
  }}
  .rank-nome-row .rank-nome-sm {{
    min-width:0; margin-bottom:0;
  }}
  .rank-cidade-r {{
    font-size:9px; font-weight:500; color:var(--texto-leve);
    background:var(--cinza); border:1px solid var(--borda);
    border-radius:3px; padding:1px 6px;
    flex-shrink:0; white-space:nowrap;
  }}

  /* ── TIPO DE CONTEÚDO ───────────────────────────────── */
  .tipo-row {{
    display:flex; align-items:center; gap:8px;
    padding:5px 0; border-bottom:1px solid #eef1f8;
  }}
  .tipo-row:last-child {{ border-bottom:none; }}
  .tipo-nome {{ font-size:11px; color:var(--texto); min-width:110px; }}
  .tipo-bar-wrap {{ flex:1; height:6px; background:#eef1f6; border-radius:3px; overflow:hidden; }}
  .tipo-bar {{ height:100%; background: linear-gradient(90deg, var(--azul-escuro), var(--azul)); border-radius:3px; }}
  .tipo-pct {{ font-family:var(--fonte-cond); font-size:13px; font-weight:700; color:var(--azul-escuro); min-width:34px; text-align:right; }}

  /* ── SEM COBERTURA ──────────────────────────────────── */
  .sem-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:6px; }}
  .sem-item {{
    display:flex; justify-content:space-between; align-items:center;
    background:#fff7f7; border:1px solid #f2d0d0;
    border-radius:5px; padding:6px 10px;
  }}
  .sem-cidade {{ font-size:11px; font-weight:500; color:var(--texto); }}
  .sem-pop {{ font-family:var(--fonte-cond); font-size:13px; font-weight:700; color:#c0392b; }}
  .sem-vazio {{ font-size:12px; color:var(--verde); font-weight:500; }}

  /* ── COLUNA ESQUERDA/DIREITA ────────────────────────── */
  .col-esq {{ display:flex; flex-direction:column; gap:18px; }}
  .col-dir {{ display:flex; flex-direction:column; gap:18px; }}

  /* ── RODAPÉ ─────────────────────────────────────────── */
  .rodape {{
    background: var(--azul-escuro);
    border-top: 3px solid var(--dourado);
    padding: 12px 24px;
    display:flex; justify-content:space-between; align-items:center;
  }}
  .rodape-texto  {{ font-size:10px; color:rgba(255,255,255,.45); }}
  .rodape-gerado {{ font-size:10px; color:rgba(255,255,255,.35); text-align:right; }}

  /* ── PRINT ──────────────────────────────────────────── */
  @media print {{
    body {{ background:white; }}
    .pagina      {{ box-shadow:none; max-width:100%; border:none; overflow:visible; }}
    .pag2        {{ break-before:page; -webkit-break-before:page; }}
    .rankings-grid .secao {{ break-inside:avoid; -webkit-break-inside:avoid; }}
    .secao  {{ break-inside:avoid; -webkit-break-inside:avoid; overflow:visible; }}
    .rodape {{ break-inside:avoid; }}
    .mapa-screen {{ display:none !important; }}
    .mapa-print  {{ display:block !important; }}
    @page   {{ size:A3 landscape; margin:8mm; }}
  }}
</style>
{('<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>' if mapa_div else '')}
</head>
<body>
<div class="pagina">

<!-- CABEÇALHO -->
<div class="cabecalho">
  <div class="cabecalho-logo">
    <img class="logo-img"
         src="https://www.alesc.sc.gov.br/wp-content/uploads/2026/01/logo_alesc_novo_2025-01.png"
         alt="Alesc"
         onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
    <div class="logo-fallback" style="display:none">
      <span class="logo-nome">ALESC</span>
      <span class="logo-sub">Assembleia Legislativa<br>de Santa Catarina</span>
    </div>
  </div>
  <div class="cabecalho-titulo">
    <div class="titulo-rel">Relatório de Desempenho · Rádio Alesc</div>
    <div class="titulo-mes">{nome_mes.upper()} / {m['ano']}</div>
    <div class="titulo-periodo">{periodo}</div>
  </div>
  <div class="cabecalho-radio">
    <div class="radio-badge">
      <div class="radio-badge-nome">RÁDIO ALESC</div>
      <div class="radio-badge-sub">Comunicação legislativa</div>
    </div>
  </div>
</div>

<!-- FAIXA INFO -->
<div class="faixa-info">
  <div class="faixa-item">Dados: <strong>Audiency Technology · {nome_mes} de {m['ano']}</strong></div>
  <div class="faixa-item">Mapa de cobertura: <strong>referência mar/2026</strong> (raio de sinal por emissora)</div>
  <div class="faixa-item">Cobertura = <strong>união dos sinais</strong> das emissoras parceiras, sem dupla contagem</div>
  <div class="faixa-item" style="margin-left:auto">Gerado em <strong>{gerado_em}</strong></div>
</div>

<!-- CARDS PRINCIPAIS -->
<div class="cards-wrap">
  <div class="card card-azul">
    <div class="card-label">Total de Veiculações</div>
    <div class="card-valor">{fmt_n(m['total_veic'])}</div>
    <div class="card-sub">
      inserções no período<br>
      <span class="delta {delta_cls}">{delta_sig} {abs(m['delta']):.1f}% vs. mês anterior</span>
    </div>
  </div>
  <div class="card card-verde">
    <div class="card-label">Municípios Alcançados</div>
    <div class="card-valor verde">{fmt_n(m['total_munis'])}</div>
    <div class="card-sub">
      de 295 municípios de SC<br>
      <span style="color:var(--verde);font-weight:600">{m['total_munis']/295*100:.0f}% dos municípios do estado</span>
    </div>
  </div>
  <div class="card card-azul">
    <div class="card-label">População Alcançada</div>
    <div class="card-valor">{fmt_pop(m['pop'])}</div>
    <div class="card-sub">
      hab. no raio de sinal<br>
      <span style="color:var(--azul);font-weight:600">{m['pct_sc']:.1f}% da população de SC</span>
    </div>
  </div>
  <div class="card card-cinza">
    <div class="card-label">Emissoras Parceiras</div>
    <div class="card-valor" style="color:#3a5470">{fmt_n(m['total_emiss'])}</div>
    <div class="card-sub">
      rádios com veiculações<br>no período analisado
    </div>
  </div>
</div>

<!-- CARDS SECUNDÁRIOS -->
<div class="cards-wrap-2">
  <div class="card-sm">
    <div class="card-sm-icon icon-azul">📅</div>
    <div class="card-sm-body">
      <div class="card-sm-label">Média Diária</div>
      <div class="card-sm-valor">{m['media_diaria']:.0f}</div>
      <div class="card-sm-sub">veiculações / dia</div>
    </div>
  </div>
  <div class="card-sm">
    <div class="card-sm-icon icon-verde">📈</div>
    <div class="card-sm-body">
      <div class="card-sm-label">Acumulado no Ano</div>
      <div class="card-sm-valor">{fmt_n(m['total_ano'])}</div>
      <div class="card-sm-sub">inserções em {m['ano']}</div>
    </div>
  </div>
  <div class="card-sm">
    <div class="card-sm-icon icon-dourado">🔊</div>
    <div class="card-sm-body">
      <div class="card-sm-label">Impressões de Audiência</div>
      <div class="card-sm-valor">{fmt_pop(m['audiencia_total'])}</div>
      <div class="card-sm-sub">exposição acumulada · não são ouvintes únicos</div>
    </div>
  </div>
  <div class="card-sm">
    <div class="card-sm-icon icon-cinza">🕐</div>
    <div class="card-sm-body">
      <div class="card-sm-label">Horário de Pico</div>
      <div class="card-sm-valor">{hora_fmt}</div>
      <div class="card-sm-sub">hora com mais veiculações</div>
    </div>
  </div>
</div>

<!-- ═══════════ PÁGINA 1: rankings ═══════════ -->
<div class="rankings-grid">

  <!-- TOP 10 CONTEÚDOS -->
  <div class="secao">
    <div class="secao-header">
      <span class="secao-titulo">10 Conteúdos com Maior Alcance Populacional</span>
      <span class="secao-badge">pop. alcançada</span>
    </div>
    <div class="secao-body">
      {rows_cont}
    </div>
  </div>

  <!-- TOP CIDADES -->
  <div class="secao">
    <div class="secao-header">
      <span class="secao-titulo">Cidades com Mais Veiculações</span>
      <span class="secao-badge">direta</span>
    </div>
    <div class="secao-body">
      {rows_cid}
    </div>
  </div>

  <!-- TOP RÁDIOS -->
  <div class="secao">
    <div class="secao-header">
      <span class="secao-titulo">Ranking de Emissoras</span>
      <span class="secao-badge">no mês</span>
    </div>
    <div class="secao-body">
      {rows_rad}
    </div>
  </div>

</div><!-- /rankings-grid pág.1 -->

<!-- ═══════════ PÁGINA 2: mapa + mesorregiões ═══════════ -->
<div class="pag2">

  <!-- MAPA LARGURA TOTAL -->
  <div class="secao" style="margin-bottom:16px">
    <div class="secao-header">
      <span class="secao-titulo">Cobertura Municipal — SC</span>
      <span class="secao-badge">{fmt_n(m['total_munis'])} de 295 municípios · {m['pct_sc']:.1f}% da população</span>
    </div>
    <div class="secao-body" style="padding:10px">
      <div class="mapa-container">
        {mapa_content}
      </div>
    </div>
  </div>

  <!-- MESORREGIÕES 3 COLUNAS -->
  <div class="secao" style="margin-bottom:16px">
    <div class="secao-header">
      <span class="secao-titulo">Cobertura por Mesorregião</span>
      <span class="secao-badge">veiculações diretas</span>
    </div>
    <div class="secao-body">
      <div class="meso-grid">
        {_meso_html(m["cob_meso"])}
      </div>
    </div>
  </div>

  <!-- NOTA METODOLÓGICA -->
  <div style="padding:10px 0 0;font-size:11px;color:#6a7d92;line-height:1.7;border-top:1px solid var(--borda);margin-top:4px">
    <strong style="color:#3a5470">Nota metodológica:</strong>
    &nbsp;<strong>Municípios alcançados</strong> = municípios no raio de sinal de cada emissora parceira (mapa mar/2026), sem dupla contagem.
    &nbsp;<strong>População alcançada</strong> = soma da população (IBGE) dos municípios alcançados.
    &nbsp;<strong>Impressões de audiência</strong> = Σ (pop. de cobertura da emissora × 80%) por veiculação — mede exposição acumulada, não ouvintes únicos; o mesmo ouvinte é contado uma vez a cada inserção que o alcança.
    &nbsp;<strong>Horário de pico</strong> = hora do dia com maior número de veiculações no período.
    &nbsp;<strong>Mesorregiões</strong> = classificação IBGE; barra = veiculações diretas, badge = municípios alcançados por sinal.
  </div>

  <div class="rodape" style="margin-top:8px">
    <div class="rodape-texto">
      Rádio Alesc · Assembleia Legislativa de Santa Catarina &nbsp;·&nbsp;
      União dos sinais sem dupla contagem &nbsp;·&nbsp;
      Pop. SC: {fmt_n(POP_SC_TOTAL)} hab.
    </div>
    <div class="rodape-gerado">Relatório de {nome_mes} de {m['ano']}</div>
  </div>

</div><!-- /pag2 -->

</div>
</body>
</html>"""

def _mapa_svg_fallback(m):
    meso_coords = {
        "Grande Florianópolis": (380, 310),
        "Norte Catarinense":    (370, 160),
        "Vale do Itajaí":       (330, 230),
        "Oeste Catarinense":    (130, 200),
        "Sul Catarinense":      (310, 390),
        "Serrana":              (210, 270),
    }
    circles = ""
    for nome_r, (cx, cy) in meso_coords.items():
        veics = m["cob_meso"].get(nome_r, {}).get("veiculacoes", 0)
        cor   = "#1a5fa8" if veics>50 else "#4a90d9" if veics>10 else "#a8c8f0" if veics>0 else "#e0e8f0"
        raio  = 28 if veics>50 else 22 if veics>10 else 16 if veics>0 else 12
        circles += (f'<circle cx="{cx}" cy="{cy}" r="{raio}" fill="{cor}" opacity="0.85"/>'
                    f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="10" fill="white" font-weight="bold">{veics}</text>')
    return f"""<svg viewBox="0 0 500 460" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:280px">
      <path d="M60,60 L480,40 L490,120 L450,200 L460,300 L420,420 L350,460 L280,440 L200,460 L120,430 L60,380 L40,280 L50,160 Z"
            fill="#dde8f5" stroke="#b0c4de" stroke-width="1.5"/>
      {circles}
    </svg>"""

# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    df   = carregar()
    mapa = carregar_abr()
    cent = _carregar_centroides()

    parser = argparse.ArgumentParser(description="Relatório mensal Rádio Alesc")
    parser.add_argument("--mes", help="Período no formato YYYY-MM (ex: --mes 2025-11)")
    parser.add_argument("--imagem", action="store_true", help="Exporta PNG além do HTML (requer Firefox)")
    args = parser.parse_args()

    anos = sorted(df["Ano"].unique())
    anos_int = [int(a) for a in anos]

    if args.mes:
        try:
            ano, mes = map(int, args.mes.split("-"))
        except ValueError:
            print("Formato inválido. Use --mes YYYY-MM  (ex: --mes 2025-11)")
            sys.exit(1)
    else:
        print(f"\nAnos disponíveis: {anos_int}")
        try:
            ano_in = input(f"Ano [{anos_int[-1]}]: ").strip()
            ano = int(ano_in) if ano_in else anos_int[-1]
            meses = sorted(int(m) for m in df[df["Ano"]==ano]["Mes"].unique())
            meses_fmt = [f"{n} ({MESES_PT[n]})" for n in meses]
            print(f"Meses em {ano}: {meses_fmt}")
            mes_in = input(f"Mês [{meses[-1]}]: ").strip()
            mes = int(mes_in) if mes_in else meses[-1]
        except (ValueError, IndexError):
            ano, mes = anos_int[-1], sorted(int(m) for m in df[df["Ano"]==anos_int[-1]]["Mes"].unique())[-1]

    print(f"\nGerando: {MESES_PT[mes]} / {ano}...")
    m = calcular(df, mapa, ano, mes)
    if not m:
        print("Sem dados para o período.")
        sys.exit(1)

    dfm = df[(df["Ano"]==ano)&(df["Mes"]==mes)].copy()
    if HAS_PLOTLY:
        print("Gerando mapa interativo (Plotly)...")
        mapa_div = gerar_mapa_mensal_div(dfm, m, cent)
    else:
        mapa_div = ""

    html  = gerar_html(m, cent, mapa_div)
    nome  = f"relatorio_radio_alesc_{MESES_PT[mes].lower()}_{ano}.html"
    caminho = OUTPUT_DIR / nome
    caminho.write_text(html, encoding="utf-8")
    print(f"\n  ✓ {caminho}  ({caminho.stat().st_size/1024:.0f} KB)")
    print("  Para PDF: abra no Chrome → Ctrl+P → Salvar como PDF → Paisagem")

    if args.imagem:
        import tempfile, shutil
        nome_png = caminho.with_suffix(".png").name
        caminho_png = OUTPUT_DIR / nome_png
        print(f"  Exportando imagem PNG ({caminho_png})...")
        # HTML temporário: oculta pág.2 (mapa) e Plotly — screenshot só da pág.1 (cards + rankings)
        estilo_img = (
            "<style>"
            ".pag2{display:none!important;}"          # oculta mapa/meso (pág 2)
            ".mapa-screen,.mapa-print{display:none!important;}"
            "body{background:#dce6f2!important;}"
            "</style></head>"
        )
        html_img = html.replace("</head>", estilo_img, 1)
        with tempfile.NamedTemporaryFile(suffix=".html", prefix="relatorio_img_", delete=False) as _f:
            tmp_html = Path(_f.name)
        tmp_html.write_text(html_img, encoding="utf-8")
        ff_profile = Path(tempfile.mkdtemp(prefix="ff-relatorio-"))
        try:
            devnull = subprocess.DEVNULL
            subprocess.run(
                ["firefox", "--headless", "--profile", str(ff_profile),
                 "--screenshot", str(caminho_png.resolve()),
                 "--window-size=1400,2000", tmp_html.resolve().as_uri()],
                stdout=devnull, stderr=devnull, timeout=45
            )
            if caminho_png.exists():
                # Recorta espaço em branco do rodapé
                try:
                    from PIL import Image as _Img
                    import numpy as _np
                    img = _Img.open(str(caminho_png)).convert("RGB")
                    arr = _np.array(img)
                    mask = (arr < 248).any(axis=2)
                    rows = _np.where(mask.any(axis=1))[0]
                    if len(rows):
                        bottom = min(int(rows[-1]) + 30, img.height)
                        img = img.crop((0, 0, img.width, bottom))
                        img.save(str(caminho_png), optimize=True)
                except Exception:
                    pass
                print(f"  ✓ {caminho_png}  ({caminho_png.stat().st_size/1024:.0f} KB)")
            else:
                print("  ✗ Exportação de imagem falhou. Verifique se o Firefox está instalado.")
        except FileNotFoundError:
            print("  ✗ Firefox não encontrado. Instale o Firefox para usar --imagem.")
        except subprocess.TimeoutExpired:
            print("  ✗ Firefox demorou demais. Tente novamente.")
        finally:
            shutil.rmtree(ff_profile, ignore_errors=True)
            tmp_html.unlink(missing_ok=True)

    try:
        devnull = subprocess.DEVNULL
        kw = dict(stdout=devnull, stderr=devnull, start_new_session=True)
        if platform.system() == "Linux":
            subprocess.Popen(["xdg-open", str(caminho)], **kw)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", str(caminho)], **kw)
    except Exception:
        pass
