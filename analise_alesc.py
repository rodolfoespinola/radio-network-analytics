import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import seaborn as sns
import requests
import unicodedata
import warnings
import json
import re
from io import StringIO
from pathlib import Path

# warnings.filterwarnings("ignore")

DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / "cache"
OUTPUT_DIR = Path("outputs")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

TAXA_ESCUTA_RADIO = 0.80 # Pesquisa ACAERT oito em cada dez catarinenses ouvem rádio - Dados de 2024
LIMIAR_LACUNA = 20_000 # Para clareza nos gráficos, considera municípios com mais de 20.000 habitantes
TOP_N_RADIOS = 10
POP_SC_TOTAL = 7_610_361 # Censo 2022

COR_PRINCIPAL  = "#1a6fa8"
COR_ALERTA     = "#c0392b"
COR_POSITIVO   = "#27ae60"
COR_SECUNDARIA = "#e07b39"
COR_MAPA_SC    = "#eaf2ea"

plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.family"] = "DejaVu Sans"
sns.set_style("whitegrid")

# Centroids dos municípios
CENTROIDES_SC_CSV = """municipio,lat,lon
Abdon Batista,-27.6097,-51.0228
Abelardo Luz,-26.5697,-52.3261
Agrolândia,-27.4058,-49.8236
Agronômica,-27.2728,-49.8583
Água Doce,-26.9944,-51.5531
Águas de Chapecó,-27.1844,-52.9878
Águas Frias,-26.8644,-52.7278
Águas Mornas,-27.7069,-48.8286
Alfredo Wagner,-27.6947,-49.3358
Alto Bela Vista,-27.3722,-52.0047
Anchieta,-26.5328,-53.3378
Angelina,-27.5750,-48.9964
Anita Garibaldi,-27.6947,-51.1303
Anitápolis,-27.9056,-49.1278
Antônio Carlos,-27.4650,-48.7508
Apiúna,-27.0397,-49.3872
Arabutã,-27.1556,-52.1539
Araquari,-26.3761,-48.7214
Araranguá,-28.9347,-49.4861
Armazém,-28.2547,-49.0128
Arroio Trinta,-26.9281,-51.3428
Arvoredo,-27.0425,-52.2889
Ascurra,-26.9747,-49.3694
Atalanta,-27.3828,-49.7878
Aurora,-27.3097,-49.6378
Balneário Arroio do Silva,-28.9833,-49.4083
Balneário Barra do Sul,-26.4572,-48.6108
Balneário Camboriú,-26.9903,-48.6347
Balneário Gaivota,-29.1167,-49.5833
Balneário Piçarras,-26.7603,-48.6708
Balneário Rincão,-28.8333,-49.2500
Bandeirante,-26.5828,-53.5714
Barra Bonita,-26.6033,-53.4944
Barra Velha,-26.6328,-48.6839
Bela Vista do Toldo,-26.0528,-50.4778
Belmonte,-26.5044,-53.4717
Benedito Novo,-26.7833,-49.3728
Biguaçu,-27.4939,-48.6558
Blumenau,-26.9194,-49.0661
Bocaina do Sul,-27.7394,-50.0044
Bom Jardim da Serra,-28.3342,-49.6258
Bom Jesus,-26.7522,-52.3894
Bom Jesus do Oeste,-26.7089,-53.0778
Bom Retiro,-27.7961,-49.4892
Bombinhas,-27.1417,-48.5153
Botuverá,-27.2028,-49.0742
Braço do Norte,-28.2742,-49.1647
Braço do Trombudo,-27.3189,-49.9200
Brunópolis,-27.3344,-51.0889
Brusque,-27.0990,-48.9167
Caçador,-26.7753,-51.0144
Caibi,-27.0628,-53.2453
Calmon,-26.5344,-51.0378
Camboriú,-27.0228,-48.6558
Campo Alegre,-26.1997,-49.2644
Campo Belo do Sul,-27.8942,-50.7644
Campo Erê,-26.3917,-53.0878
Campos Novos,-27.4025,-51.2253
Canelinha,-27.2694,-48.7747
Canoinhas,-26.1806,-50.3900
Capão Alto,-28.0208,-50.5011
Capinzal,-27.3408,-51.6158
Capivari de Baixo,-28.4458,-49.0011
Catanduvas,-27.0728,-51.6578
Caxambu do Sul,-27.1503,-52.8644
Celso Ramos,-27.6286,-51.3017
Cerro Negro,-27.7700,-50.8700
Chapadão do Lageado,-27.5628,-49.6997
Chapecó,-27.1003,-52.6150
Cocal do Sul,-28.6025,-49.3258
Concórdia,-27.2342,-52.0278
Cordilheira Alta,-27.2028,-52.6489
Coronel Freitas,-26.9044,-52.7214
Coronel Martins,-26.5514,-52.6289
Correia Pinto,-27.5858,-50.3608
Corupá,-26.4264,-49.2411
Criciúma,-28.6775,-49.3697
Cunha Porã,-26.8931,-53.1736
Cunhataí,-26.9439,-53.1178
Curitibanos,-27.2825,-50.5831
Descanso,-26.8228,-53.5017
Dionísio Cerqueira,-26.2550,-53.6369
Dona Emma,-26.9294,-49.5208
Doutor Pedrinho,-26.7422,-49.4783
Entre Rios,-26.7044,-52.5528
Ermo,-28.9894,-49.6814
Erval Velho,-27.2797,-51.4539
Faxinal dos Guedes,-26.8500,-52.2581
Flor do Sertão,-26.7044,-53.4028
Florianópolis,-27.5954,-48.5480
Formosa do Sul,-26.6578,-52.8578
Forquilhinha,-28.7453,-49.4728
Fraiburgo,-27.0228,-50.9192
Frei Rogério,-27.1736,-50.8278
Galvão,-26.4339,-52.5578
Garopaba,-28.0239,-48.6228
Garuva,-26.0331,-48.8508
Gaspar,-26.9314,-48.9578
Governador Celso Ramos,-27.3183,-48.5578
Grão Pará,-28.1764,-49.2297
Gravatal,-28.3228,-49.0458
Guabiruba,-27.0636,-48.9836
Guaraciaba,-26.5947,-53.5228
Guaramirim,-26.4728,-48.9978
Guarujá do Sul,-26.3828,-53.5194
Guatambú,-27.1506,-52.7983
Herval d'Oeste,-27.1906,-51.4869
Ibiam,-27.2653,-51.4808
Ibicaré,-27.0819,-51.3517
Ibirama,-27.0572,-49.5178
Içara,-28.7133,-49.3036
Ilhota,-26.8994,-48.8283
Imaruí,-28.3292,-48.8197
Imbituba,-28.2406,-48.6658
Imbuia,-27.4878,-49.5228
Indaial,-26.8978,-49.2333
Iomerê,-27.0022,-51.2428
Ipira,-27.3978,-51.7878
Iporã do Oeste,-26.9978,-53.5325
Ipuaçu,-26.6428,-52.4678
Ipumirim,-27.0714,-52.0928
Iraceminha,-26.8228,-53.2778
Irani,-27.0303,-51.8717
Irati,-26.5344,-52.4678
Irineópolis,-26.2344,-50.7894
Itá,-27.2906,-52.3244
Itaiópolis,-26.3378,-49.9083
Itajaí,-26.9078,-48.6619
Itapema,-27.0861,-48.6147
Itapiranga,-27.1681,-53.7108
Itapoá,-26.1244,-48.6139
Ituporanga,-27.4128,-49.5978
Jaborá,-27.1797,-51.7378
Jacinto Machado,-28.9981,-49.7614
Jaguaruna,-28.6128,-49.0297
Jaraguá do Sul,-26.4853,-49.0689
Jardinópolis,-26.7228,-52.9278
Joaçaba,-27.1742,-51.5044
Joinville,-26.3044,-48.8487
José Boiteux,-27.0028,-49.6478
Jupiá,-26.4144,-52.9028
Lacerdópolis,-27.2497,-51.5544
Lages,-27.8158,-50.3258
Laguna,-28.4808,-48.7811
Lajeado Grande,-26.7678,-52.4878
Laurentino,-27.2233,-49.7378
Lauro Müller,-28.3892,-49.3997
Lebon Régis,-26.9256,-50.6917
Leoberto Leal,-27.6219,-49.1528
Lindóia do Sul,-27.0519,-52.1497
Lontras,-27.1578,-49.5303
Luiz Alves,-26.7158,-48.9250
Luzerna,-27.1294,-51.4742
Macieira,-26.7906,-51.3128
Mafra,-26.1097,-49.8019
Major Gercino,-27.4361,-48.9119
Major Vieira,-26.3694,-50.3233
Maracajá,-28.8328,-49.4458
Maravilha,-26.7692,-53.1717
Marema,-26.9044,-52.5878
Massaranduba,-26.6086,-49.0075
Matos Costa,-26.4728,-51.1544
Meleiro,-28.8278,-49.6358
Mirim Doce,-27.1611,-50.0867
Modelo,-26.7819,-53.0239
Mondaí,-27.0975,-53.4044
Monte Carlo,-27.2278,-50.9628
Monte Castelo,-26.4578,-50.2244
Morro da Fumaça,-28.6544,-49.2278
Morro Grande,-28.7667,-49.7000
Navegantes,-26.8994,-48.6539
Nova Erechim,-26.9000,-52.9097
Nova Itaberaba,-26.9406,-52.8408
Nova Trento,-27.2883,-48.9278
Nova Veneza,-28.6381,-49.5025
Novo Horizonte,-26.4578,-52.8100
Orleans,-28.3600,-49.2958
Otacílio Costa,-27.4786,-50.1228
Ouro,-27.3544,-51.6178
Ouro Verde,-26.6978,-52.3028
Paial,-27.2478,-52.4378
Painel,-28.0019,-50.1006
Palhoça,-27.6447,-48.6658
Palma Sola,-26.3525,-53.2869
Palmeira,-27.9236,-50.1583
Palmitos,-27.0711,-53.1578
Papanduva,-26.3822,-50.1478
Paraíso,-26.6111,-53.2897
Passo de Torres,-29.3244,-49.7178
Passos Maia,-26.7844,-51.9244
Paulo Lopes,-27.9617,-48.6808
Pedras Grandes,-28.4489,-49.1900
Penha,-26.7711,-48.6447
Peritiba,-27.4278,-51.9428
Pescaria Brava,-28.3833,-48.8667
Petrolândia,-27.5317,-49.6878
Pinhalzinho,-26.8472,-52.9869
Pinheiro Preto,-27.0814,-51.2183
Piratuba,-27.4228,-51.7728
Planalto Alegre,-27.0428,-52.7739
Pomerode,-26.7428,-49.1756
Ponte Alta,-27.4869,-50.3814
Ponte Alta do Norte,-27.1542,-50.4553
Ponte Serrada,-26.8694,-52.0158
Porto Belo,-27.1558,-48.5508
Porto União,-26.2331,-51.0794
Pouso Redondo,-27.2578,-49.9478
Praia Grande,-29.1928,-49.9578
Presidente Castello Branco,-27.1778,-51.7244
Presidente Getúlio,-27.0478,-49.6247
Presidente Nereu,-27.2528,-49.7478
Princesa,-26.4539,-53.5494
Quilombo,-26.7306,-52.7244
Rancho Queimado,-27.6828,-49.0119
Rio das Antas,-26.8942,-51.0817
Rio do Campo,-26.9578,-50.1428
Rio do Oeste,-27.1933,-49.7978
Rio do Sul,-27.2147,-49.6436
Rio dos Cedros,-26.7458,-49.2747
Rio Fortuna,-28.1728,-49.1042
Rio Negrinho,-26.2553,-49.5197
Rio Rufino,-27.8786,-49.9000
Riqueza,-27.0814,-53.3367
Rodeio,-26.9239,-49.3528
Romelândia,-26.6828,-53.3517
Salete,-26.9828,-49.6878
Saltinho,-26.5847,-52.6553
Salto Veloso,-26.9553,-51.2019
Sangão,-28.5656,-49.1264
Santa Cecília,-26.9594,-50.4247
Santa Helena,-26.9378,-53.6183
Santa Rosa de Lima,-28.0356,-49.1378
Santa Rosa do Sul,-29.1244,-49.7358
Santa Terezinha,-26.7806,-50.0278
Santa Terezinha do Progresso,-26.8236,-53.1978
Santiago do Sul,-26.5678,-52.5278
Santo Amaro da Imperatriz,-27.6836,-48.7906
São Bento do Sul,-26.2500,-49.3797
São Bernardino,-26.4528,-52.8778
São Bonifácio,-27.9053,-48.9378
São Carlos,-27.0778,-53.0478
São Cristóvão do Sul,-27.2967,-50.3728
São Domingos,-26.5647,-52.5344
São Francisco do Sul,-26.2433,-48.6397
São João Batista,-27.2728,-48.8483
São João do Itaperiú,-26.6558,-48.7753
São João do Oeste,-27.0903,-53.5581
São João do Sul,-29.2458,-49.8078
São Joaquim,-28.2942,-49.9317
São José,-27.6136,-48.6369
São José do Cedro,-26.4700,-53.5528
São José do Cerrito,-27.6528,-50.5817
São Lourenço do Oeste,-26.3578,-52.8478
São Ludgero,-28.3158,-49.1697
São Martinho,-28.1353,-49.1267
São Miguel da Boa Vista,-26.7539,-53.4017
São Miguel do Oeste,-26.7278,-53.5139
São Pedro de Alcântara,-27.5847,-48.8028
Saudades,-26.9353,-53.0028
Schroeder,-26.4153,-49.0681
Seara,-27.1503,-52.3167
Serra Alta,-26.7278,-52.8678
Siderópolis,-28.5981,-49.4258
Sombrio,-29.1058,-49.6333
Sul Brasil,-26.7214,-52.9678
Taió,-27.1144,-49.9994
Tangará,-27.1022,-51.2494
Tigrinhos,-26.7139,-53.2878
Tijucas,-27.2422,-48.6344
Timbé do Sul,-28.9781,-49.8261
Timbó,-26.8228,-49.2717
Timbó Grande,-26.6144,-50.9028
Três Barras,-26.1208,-50.3133
Treviso,-28.5406,-49.4928
Treze de Maio,-28.5658,-49.1856
Treze Tílias,-26.6044,-51.4017
Tubarão, -28.4678,-49.0128
Tunápolis,-26.9828,-53.6178
Turvo,-28.9258,-49.6897
União do Oeste,-26.7928,-52.8378
Urubici,-28.0158,-49.5919
Urupema,-28.0006,-49.8767
Urussanga,-28.5200,-49.3228
Vargeão,-26.8339,-52.1300
Vargem,-27.5506,-50.8600
Vargem Bonita,-26.9878,-52.0008
Vidal Ramos,-27.3897,-49.3578
Videira,-27.0078,-51.1536
Vitor Meireles,-26.8933,-49.7367
Witmarsum,-27.3278,-49.5578
Xanxerê,-26.8758,-52.4031
Xavantina,-27.0617,-52.3478
Xaxim,-26.9606,-52.5369
Zortéa,-27.4722,-51.5531
"""

# Colocando os centroids em um CSV insline
df_centroides = pd.read_csv(StringIO(CENTROIDES_SC_CSV)) # Pega a variável e faz agir como arquivo real
# Normalização - transforma em texto, minúsculo, remove espaços, decompõe caracteres
df_centroides["Cidade_norm"] = df_centroides["municipio"].apply(
    lambda x: unicodedata.normalize("NFD", str(x).lower().strip())
              .encode("ascii", "ignore").decode()
)

# ----Funções----

# Criar chaves de busca
def normalizar(texto):
    if pd.isna(texto):
        return ""
    texto = str(texto).lower().strip()
    texto = texto.replace("-", " ").replace("'", " ")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn") # "Mn" Mark, Nonspacing (acentos e sinais)

# Extrair data
def extrair_data_criacao(nome):
    if pd.isna(nome):
        return pd.NaT
    nome = str(nome).strip()
    nome = re.sub(r'[_\s]+[cC]$', '', nome).strip()

    todas = re.findall(r'\d{8}', nome)
    if todas:
        seq = todas[-1]
        d, mes, ano = int(seq[0:2]), int(seq[2:4]), int(seq[4:8])
        # Tenta formato BR: DDMMYYYY
        if 1 <= d <= 31 and 1 <= mes <= 12 and 2020 <= ano <= 2030:
            try:
                return pd.Timestamp(f'{ano}-{mes:02d}-{d:02d}')
            except:
                pass
        # Tenta formato americano: MMDDYYYY (mês > 12 no BR = americano)
        mes_us, d_us, ano_us = int(seq[0:2]), int(seq[2:4]), int(seq[4:8])
        if 1 <= mes_us <= 12 and 1 <= d_us <= 31 and 2020 <= ano_us <= 2030:
            try:
                return pd.Timestamp(f'{ano_us}-{mes_us:02d}-{d_us:02d}')
            except:
                pass

    todas6 = re.findall(r'\d{6}', nome)
    if todas6:
        seq = todas6[-1]
        d, mes, ano = int(seq[0:2]), int(seq[2:4]), 2000 + int(seq[4:6])
        if 1 <= d <= 31 and 1 <= mes <= 12 and 2020 <= ano <= 2030:
            try:
                return pd.Timestamp(f'{ano}-{mes:02d}-{d:02d}')
            except:
                pass

    return pd.NaT

# Limpar para exibição em gráficos
def normalizar_nomenclatura(nome):
    if pd.isna(nome):
        return nome
    return str(nome).replace("_", " ").strip()

def categorizar_tipo(nome):
    if pd.isna(nome):
        return "Sem categoria"
    nome_norm = normalizar_nomenclatura(nome)
    prefixo = nome_norm.strip().upper().split()[0] if nome_norm.strip() else ""
    mapa = {
        # Ordem do Dia
        "OD":           "Ordem do Dia",
        "ODT":          "Ordem do Dia",
        "ORDEM":        "Ordem do Dia",
        # Projetos de Lei
        "PL":           "Projeto de Lei",
        "PEC":          "Projeto de Lei",
        "PLS":          "Projeto de Lei",
        # Comissões
        "COM":          "Comissão",
        "CCJ":          "Comissão",
        "COMISSÃO":     "Comissão",
        "COMISSAO":     "Comissão",
        # Sessões
        "SESSAO":       "Sessão",
        "SESSÃO":       "Sessão",
        "SOLENE":       "Sessão",
        # Frentes Parlamentares e Bancadas
        "FP":           "Frentes e Bancadas",
        "FRENTE":       "Frentes e Bancadas",
        "BANCADA":      "Frentes e Bancadas",
        # Audiências Públicas
        "AP":           "Audiência Pública",
        "AUD":          "Audiência Pública",
        "AUDIENCIA":    "Audiência Pública",
        "AUDIÊNCIA":    "Audiência Pública",
        # Eventos
        "EVENTO":       "Evento",
        "SEMINÁRIO":    "Evento",
        "SEMINARIO":    "Evento",
        "PALESTRA":     "Evento",
        "ROMARIA":      "Evento",
        "FESTA":        "Evento",
        "FÓRUM":        "Evento",
        "FORUM":        "Evento",
        "LIVRO":        "Evento",
        # Legislação sancionada / executivo
        "SANCIONADOS":  "Legislação",
        "SANÇÃO":       "Legislação",
        "INFORMATIVO":  "Legislação",
        "VETO":         "Legislação",
        "DECRETO":      "Legislação",
        # Informativo / institucional
        "INSTITUCIONAL":"Institucional",
        "CHAMADA":      "Institucional",
        #Podcast
        "POD":          "Podcast",
        "RF":           "Podcast",
        # Outros tipos mapeáveis
        "PLE":          "Plenário",
        "SUSP":         "Plenário",
        "MOÇÃO":        "Moção",
        "MOCAO":        "Moção",
        "ESPECIAL":     "Especial",
        "PRES":         "Outros",
    }
    return mapa.get(prefixo, "Outros")

def salvar(fig, nome):
    fig.savefig(OUTPUT_DIR / nome, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {nome}")

def nota_rodape(ax, texto):
    ax.text(0.99, 0.01, texto, transform=ax.transAxes,
            ha="right", fontsize=7, color="#888", style="italic")

def gini(valores):
    """
    Calcula o Coeficiente de Gini para medir a concentração/desigualdade.
    
    O índice varia de 0 a 1, onde:
    - 0: Igualdade perfeita (ex: todas as rádios têm a mesma audiência).
    - 1: Desigualdade máxima (ex: uma única rádio detém toda a audiência).
    
    Útil para avaliar a democratização da informação e a cobertura regional da ALESC.
    """
    v = sorted(valores)
    n = len(v)
    if n == 0 or sum(v) == 0:
        return 0
    cumsum = sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(v))
    return cumsum / (n * sum(v))

def buscar_com_cache(url, cache_path, timeout=15):
    """Busca URL com cache local. Usa cache se existir e API falhar."""
    if cache_path.exists():
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            cache_path.write_text(r.text, encoding="utf-8")
            return r.json()
        except Exception:
            print(f"  ⚠ API indisponível — usando cache: {cache_path.name}")
            return json.loads(cache_path.read_text(encoding="utf-8"))
    else:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        cache_path.write_text(r.text, encoding="utf-8")
        return r.json()

# ══════════════════════════════════════════════════════════════════════════════
# 1. VALIDAÇÃO DOS DATASETS
# ══════════════════════════════════════════════════════════════════════════════

print("\n[1/8] Validando datasets...")

arquivos = sorted(DATA_DIR.glob("*.xlsx"))
if not arquivos:
    raise FileNotFoundError(f"Nenhum .xlsx em '{DATA_DIR}/'")

COLUNAS = ["Identificador", "Data", "Hora", "Radio", "Cidade_UF", "Peca", "Comercial"]
relatorio_val, dfs, erros = [], [], []

for arq in arquivos:
    try:
        tmp = pd.read_excel(arq, header=None)

        # Detecta cabeçalho verificando coluna B (coluna A pode ter número aleatório)
        if str(tmp.iloc[0, 1]).strip().lower() == "data":
            # Linha 0 = cabeçalho, linha 1 = vazia — pula as duas
            tmp = tmp.iloc[2:].reset_index(drop=True)
        # else: linha 0 já é dado, usa como está

        tmp.columns = COLUNAS[:len(tmp.columns)]
        tmp["Veiculacoes"] = 1

        # Remove linhas completamente vazias
        tmp = tmp.dropna(subset=[tmp.columns[0]])

        datas = pd.to_datetime(tmp["Data"], dayfirst=True, errors="coerce", format="mixed")
        pct_inv = datas.isna().mean() * 100
        amostra = tmp["Comercial"].dropna().head(50)
        sep = "underscore" if amostra.str.contains("_", na=False).mean() > 0.5 else "espaço"

        tmp["Arquivo"] = arq.name
        dfs.append(tmp)
        relatorio_val.append({
            "Arquivo": arq.name, "Registros": len(tmp),
            "Separador": sep,
            "Datas_invalidas_pct": f"{pct_inv:.1f}%",
            "Status": "OK" if pct_inv < 5 else f"⚠ {pct_inv:.0f}% datas inválidas",
        })
    except Exception as e:
        erros.append(arq.name)
        print(f"  ✗ ERRO em {arq.name}: {e}")
        relatorio_val.append({"Arquivo": arq.name, "Registros": 0,
                       "Separador": "—",
                       "Datas_invalidas_pct": "—",
                       "Status": f"ERRO: {e}"})

df_val = pd.DataFrame(relatorio_val)
print(df_val[["Arquivo","Registros","Separador","Status"]].to_string(index=False))
df_val.to_csv(OUTPUT_DIR / "00_relatorio_validacao.csv", index=False)

# ══════════════════════════════════════════════════════════════════════════════
# 2. CONSOLIDAÇÃO E LIMPEZA
# ══════════════════════════════════════════════════════════════════════════════

print("\n[2/8] Consolidando dados...")

df = pd.concat(dfs, ignore_index=True)
df[["Cidade", "UF"]] = df["Cidade_UF"].str.extract(r"^(.+?)\s*/\s*(\w{2})$")
df["UF"] = df["Cidade_UF"].str.extract(r"/\s*(\w{2})$")[0].str.strip().fillna("SC")
df["Cidade"]         = df["Cidade"].str.strip()
df["Data"]           = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce", format="mixed")
df                   = df.dropna(subset=["Data"])
df["Ano"]            = df["Data"].dt.year.astype(int)
df["Mes"]            = df["Data"].dt.month
df["AnoMes"]         = df["Data"].dt.to_period("M")
df["Hora_dt"]        = pd.to_datetime(df["Hora"], format="%H:%M:%S", errors="coerce")
df["Hora_int"]       = df["Hora_dt"].dt.hour
df["Tipo"]           = df["Comercial"].apply(categorizar_tipo)
df["Cidade_norm"]    = df["Cidade"].apply(normalizar)
df["Data_Criacao"] = df["Comercial"].apply(extrair_data_criacao)
df["Data_Criacao"] = pd.to_datetime(df["Data_Criacao"], errors="coerce")
df["Dias_Ate_Veiculacao"] = (df["Data"] - df["Data_Criacao"]).dt.days


# --- LIMPEZA DE DADOS  ---

# 1. Elimina as linhas de rodapé 
# Se a Cidade_UF for nula, a linha é descartada
df = df.dropna(subset=["Cidade_UF"])

anos = sorted(df["Ano"].unique())
print(f"  ✓ {len(df):,} registros | {df['Radio'].nunique()} rádios | "
      f"{df['Cidade'].nunique()} cidades | {anos}")
for ano in anos:
    print(f"    {ano}: {(df['Ano']==ano).sum():,} veiculações")

# Remove casos inválidos (data criação > data veiculação = erro de extração)
df_ciclo = df[
    df["Dias_Ate_Veiculacao"].notna() &
    (df["Dias_Ate_Veiculacao"] >= 0) &
    (df["Dias_Ate_Veiculacao"] <= 365)  # ignora outliers absurdos
].copy()

pct_ciclo = len(df_ciclo) / len(df) * 100
print(f"  ✓ Ciclo de vida: {len(df_ciclo):,} registros com data extraída ({pct_ciclo:.1f}%)")
# ══════════════════════════════════════════════════════════════════════════════
# 3. POPULAÇÃO IBGE (com cache)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3/8] Dados IBGE...")

# Cidades de fronteira
CIDADES_FRONTEIRA = {
    "rio negro":                 {"pop": 33_172, "lat": -26.1003, "lon": -49.7931},
    "uniao da vitoria":          {"pop": 57_768, "lat": -26.2278, "lon": -51.0872},
    "santo antonio do sudoeste": {"pop": 20_748, "lat": -26.3589, "lon": -53.7561},
}


df_pop = None
cache_path = CACHE_DIR / "ibge_populacao_sc.json"

try:
    if cache_path.exists():
        dados = json.loads(cache_path.read_text(encoding="utf-8"))
        print(f"  ✓ Usando cache: {cache_path.name}")
    else:
        url = ("https://servicodados.ibge.gov.br/api/v3/agregados/6579"
               "/periodos/2021/variaveis/9324?localidades=N6[in N3[42]]")
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        dados = r.json()
        cache_path.write_text(json.dumps(dados), encoding="utf-8")
        print("  ✓ População IBGE: carregada via API")

    registros = []
    for item in dados[0]["resultados"][0]["series"]:
        nome = item["localidade"]["nome"].replace(" - SC", "").strip()
        pop = item["serie"].get("2021")
        if pop:
            registros.append({"Municipio_IBGE": nome, "Populacao": int(pop)})

    df_pop = pd.DataFrame(registros)
    df_pop["Cidade_norm"] = df_pop["Municipio_IBGE"].apply(normalizar)
    print(f"  ✓ {len(df_pop)} municípios SC com população")

    extras_pop = pd.DataFrame([
        {"Municipio_IBGE": k, "Cidade_norm": k, "Populacao": v["pop"]}
        for k, v in CIDADES_FRONTEIRA.items()
    ])
    df_pop = pd.concat([df_pop, extras_pop], ignore_index=True)
    print(f"  ✓ {len(CIDADES_FRONTEIRA)} cidades de fronteira (PR) adicionadas")

except Exception as e:
    print(f"  ⚠ População IBGE indisponível: {e}")

# Merge população — fallback usa mediana estadual
"""
if df_pop is not None:
    df = df.merge(df_pop[["Cidade_norm", "Populacao"]], on="Cidade_norm", how="left")
    mediana_pop = df_pop["Populacao"].median()
    sem_match_mask = df_pop["Populacao"].isna() # Identifica registros sem match
    n_sem_match = df["Populacao"].isna().sum()
    df["Populacao"] = df["Populacao"].fillna(mediana_pop)
    if n_sem_match > 0:
        print(f"  ⚠ {n_sem_match} registros sem match — fallback mediana "
              f"estadual ({mediana_pop:,.0f} hab.)")
else:
    df["Populacao"] = 12_000   # mediana aproximada SC
"""
if df_pop is not None:
    df = df.merge(df_pop[["Cidade_norm", "Populacao"]], on="Cidade_norm", how="left")
    mediana_pop = df_pop["Populacao"].median()
    sem_match_mask = df["Populacao"].isna()          # captura ANTES do fillna
    n_sem_match = sem_match_mask.sum()
    df["Populacao"] = df["Populacao"].fillna(mediana_pop)
    if n_sem_match > 0:
        print(f"  ⚠ [PATCH 4] {n_sem_match} registros sem match IBGE — "
              f"fallback mediana estadual ({mediana_pop:,.0f} hab.)")
        cidades_sem_match = df[sem_match_mask]["Cidade_UF"].unique()
        for c in sorted(cidades_sem_match)[:10]:
            print(f"    → {c}")
    else:
        print("  ✓ [PATCH 4] Todas as cidades com match no IBGE")
else:
    sem_match_mask = pd.Series(False, index=df.index)
    df["Populacao"] = 12_000

df["Audiencia_Unica"] = df["Populacao"] * TAXA_ESCUTA_RADIO

# Merge centroides — 294 municípios embutidos
df_centroides["Cidade_norm"] = df_centroides["municipio"].apply(normalizar)
print(f"  ✓ Centroides: {len(df_centroides)} municípios (embutidos)")

# Centroides de cidades de fronteira
extras_centroides = pd.DataFrame([
    {"municipio": k, "Cidade_norm": k, "lat": v["lat"], "lon": v["lon"]}
    for k, v in CIDADES_FRONTEIRA.items()
])
df_centroides = pd.concat([df_centroides, extras_centroides], ignore_index=True)
print(f"  ✓ Centroides: {len(df_centroides)} municípios (SC + fronteira PR)")


# --- DIAGNÓSTICO DE ERROS ---

print("\n🔍 Investigando cidades sem match no IBGE (Top 10):")
cidades_erro = df[df["Populacao"] == 8054]["Cidade_UF"].unique()
print(cidades_erro[:10])

# ── Sanity check geográfico ───────────────────────────────────────────────
cidades_excel     = set(df["Cidade_norm"].dropna().unique())
cidades_mapa      = set(df_centroides["Cidade_norm"].unique())
cidades_faltantes = cidades_excel - cidades_mapa
if cidades_faltantes:
    print(f"  ⚠ {len(cidades_faltantes)} cidades sem centroide (não plotadas):")
    for c in sorted(cidades_faltantes)[:15]:
        print(f"    → {c}")
    (df[df["Cidade_norm"].isin(cidades_faltantes)][["Cidade", "Cidade_norm", "Radio"]]
     .drop_duplicates()
     .sort_values("Cidade")
     .to_csv(OUTPUT_DIR / "erros_geograficos.csv", index=False, encoding="utf-8-sig"))
    print("  ✓ erros_geograficos.csv exportado")
else:
    print("  ✓ 100% das cidades com centroide")
# ----------------------------

# ══════════════════════════════════════════════════════════════════════════════
# 4. TABELAS BASE
# ══════════════════════════════════════════════════════════════════════════════

alcance = (
    df.groupby(["Cidade", "Cidade_norm"])
    .agg(Veiculacoes=("Identificador","count"),
         Populacao=("Populacao","first"),
         Audiencia_Unica=("Audiencia_Unica","first"))
    .reset_index()
)
alcance["Alcance_Ponderado"]  = alcance["Veiculacoes"] * alcance["Populacao"] # Total
alcance["Indice_Intensidade"] = alcance["Veiculacoes"] / alcance["Populacao"] * 10_000 # Quantas veiculações para cada 10.000 habitantes
alcance["Impacto_Radio"]      = alcance["Alcance_Ponderado"]  # alias semântico

alcance = alcance.merge(df_centroides[["Cidade_norm","lat","lon"]],
                        on="Cidade_norm", how="left")

serie_mensal = df.groupby("AnoMes").size().reset_index(name="Veiculacoes")
tipo_count   = df["Tipo"].value_counts()

# Cobertura e lacunas
cidades_cobertas = set(df["Cidade_norm"].dropna().unique())
lacunas = pd.DataFrame()
if df_pop is not None:
    df_pop["tem_cobertura"] = df_pop["Cidade_norm"].isin(cidades_cobertas)
    lacunas = (df_pop[~df_pop["tem_cobertura"]]
               .query(f"Populacao > {LIMIAR_LACUNA}")
               .sort_values("Populacao", ascending=False).head(15))

# Evolução de cobertura por ano
cobertura_ano = (df.groupby("Ano")["Cidade"].nunique()
                   .reset_index(name="Municipios_Alcancados"))
if df_pop is not None:
    pop_coberta_ano = []
    for ano in anos:
        cidades_ano = set(df[df["Ano"]==ano]["Cidade_norm"].dropna().unique())
        pop = df_pop[df_pop["Cidade_norm"].isin(cidades_ano)]["Populacao"].sum()
        pop_coberta_ano.append({"Ano": ano, "Pop_Coberta": pop})
    cobertura_ano = cobertura_ano.merge(pd.DataFrame(pop_coberta_ano), on="Ano")
    cobertura_ano["Pct_Pop_SC"] = cobertura_ano["Pop_Coberta"] / POP_SC_TOTAL * 100 # Aqui conseguimos o percentual da população

# Gini
# Se o Gini for próximo de 0, as inserções estão bem distribuídas por todo o estado. Se for próximo de 1, significa que pouquíssimas cidades (provavelmente as maiores) estão recebendo quase todo o conteúdo, enquanto o interior está "no silêncio".
gini_val = gini(alcance["Veiculacoes"].tolist())

# Churn
# Fidelidade de rádios parceiras
""""
radios_por_ano = df.groupby("Ano")["Radio"].apply(set)
churn_data = []
for i in range(1, len(anos)):
    a_ant, a_cur = anos[i-1], anos[i]
    entradas = radios_por_ano[a_cur] - radios_por_ano[a_ant]
    saidas   = radios_por_ano[a_ant] - radios_por_ano[a_cur]
    churn_data.append({"Ano": a_cur, "Entradas": len(entradas),
                       "Saidas": -len(saidas)})
df_churn = pd.DataFrame(churn_data)
"""
historico_total = set()
anos_lista = sorted(df["Ano"].unique())
historico_acumulado = set()
churn_data = []

for i, ano in enumerate(anos_lista):
    radios_deste_ano = set(df[df["Ano"] == ano]["Radio"])
    
    if i == 0:
        # No primeiro ano, todas as rádios são novas entradas
        novas = len(radios_deste_ano)
        saidas = 0
    else:
        # NOVAS: Rádios que nunca apareceram em nenhum ano anterior (Crescimento Real)
        novas_set = radios_deste_ano - historico_acumulado
        novas = len(novas_set)
        
        # INATIVAS: Rádios que já foram parceiras mas não veicularam nada ESTE ano
        saidas_set = historico_acumulado - radios_deste_ano
        saidas = len(saidas_set)
        
    # Atualiza o histórico para incluir as rádios deste ano
    historico_acumulado.update(radios_deste_ano)
    
    churn_data.append({
        "Ano": ano,
        "Novas": novas,
        "Saidas": -saidas, # Negativo para o efeito visual de 'espelho' no gráfico
        "Total_Ativas": len(radios_deste_ano)
    })

df_churn = pd.DataFrame(churn_data)

# Fidelidade
# Possibilidade de criar um ranking chamado "Emissoras Diamante", filtrando apenas as rádios que têm Anos_Ativo > 2 e Taxa_Fidelidade == 100
radio_ano = df.groupby(["Radio","Ano"]).size().reset_index(name="Veiculacoes")
fidelidade = (
    radio_ano.groupby("Radio")
    .agg(Anos_Ativo=("Ano","nunique"), Total_Veiculacoes=("Veiculacoes","sum"),
         Primeiro_Ano=("Ano","min"), Ultimo_Ano=("Ano","max"))
    .reset_index()
)
fidelidade["Anos_Possiveis"]  = fidelidade["Ultimo_Ano"] - fidelidade["Primeiro_Ano"] + 1 # Para não punir rádios novas
fidelidade["Taxa_Fidelidade"] = fidelidade["Anos_Ativo"] / fidelidade["Anos_Possiveis"] * 100 # Percentual de fidelidade

# Ranking de rádios por impacto
impacto_radio = (
    df.merge(alcance[["Cidade","Populacao"]], on="Cidade", how="left", suffixes=("","_a"))
    .groupby("Radio")
    .agg(Veiculacoes=("Identificador","count"),
         Impacto=("Populacao","sum")) # soma a população da cidade toda vez que a rádio toca nela
    .reset_index()
    .sort_values("Impacto", ascending=False)
)

# Ciclo de vida por tipo de conteúdo
ciclo_tipo = (
    df_ciclo.groupby("Tipo")["Dias_Ate_Veiculacao"]
    .agg(
        Media_dias   = "mean",
        Mediana_dias = "median",
        Max_dias     = "max",
        Veiculacoes  = "count",
    )
    .round(1)
    .sort_values("Mediana_dias", ascending=False)
    .reset_index()
)

# Ciclo de vida por comercial individual (os mais longevos)
ciclo_comercial = (
    df_ciclo.groupby("Comercial")["Dias_Ate_Veiculacao"]
    .agg(
        Primeira_veiculacao = "min",
        Ultima_veiculacao   = "max",
        Total_veiculacoes   = "count",
        Vida_util_dias      = lambda x: x.max() - x.min(),
    )
    .sort_values("Vida_util_dias", ascending=False)
    .reset_index()
)

# Zumbis: comerciais com veiculações após 30 dias da criação
zumbis = df_ciclo[df_ciclo["Dias_Ate_Veiculacao"] > 30].groupby("Comercial").agg(
    Veiculacoes_tardias = ("Comercial", "count"),
    Max_dias            = ("Dias_Ate_Veiculacao", "max"),
    Tipo                = ("Tipo", "first"),
).sort_values("Max_dias", ascending=False).reset_index()

# ══════════════════════════════════════════════════════════════════════════════
# 5. VISUALIZAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
print("\n[4/8] Gerando gráficos...")

mapa_df = alcance.dropna(subset=["lat","lon"]).copy()

# ── 01 Mapa de cobertura ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
for ax, col, titulo, cmap_n, label in [
    (axes[0],"Veiculacoes","Veiculações por Município","Blues","Veiculações"),
    (axes[1],"Audiencia_Unica",f"Audiência Única Estimada*","Oranges","Pessoas"),
]:
    ax.set_facecolor("#f0f4f8")
    if len(mapa_df) > 0:
        vals = mapa_df[col]
        norm = mcolors.LogNorm(vmin=max(vals.min(),1), vmax=vals.max())
        sc = ax.scatter(mapa_df["lon"], mapa_df["lat"], c=vals, cmap=cmap_n,
                        norm=norm, s=mapa_df["Populacao"]/3000,
                        alpha=0.85, edgecolors="white", linewidths=0.4, zorder=2)
        plt.colorbar(sc, ax=ax, label=label, fraction=0.03, pad=0.04)
        for _, row in mapa_df.nlargest(5, col).iterrows():
            ax.annotate(row["Cidade"], (row["lon"], row["lat"]),
                        fontsize=6.5, ha="center",
                        xytext=(0,7), textcoords="offset points", color="#222", zorder=3)
    ax.set_title(titulo, fontweight="bold", fontsize=11)
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
fig.suptitle("Mapa de Cobertura da Rádio Alesc — Santa Catarina\n"
             "(tamanho proporcional à população)", fontweight="bold")
nota_rodape(axes[1], f"*Audiência única = pop. × {TAXA_ESCUTA_RADIO} (penetração rádio IBOPE/Kantar)")
fig.tight_layout()
salvar(fig, "01_mapa_cobertura_sc.png")

# ── 02 NOVO: Evolução de cobertura territorial por ano ────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 7)) 

x = [str(a) for a in cobertura_ano["Ano"]]
largura_barra = 0.6

# 1. BARRAS: Usamos uma cor sólida mas suave para o fundo não "gritar"
bars = ax1.bar(x, cobertura_ano["Municipios_Alcancados"],
               color=COR_PRINCIPAL, alpha=0.3, label="Municípios", width=largura_barra)

ax1.set_ylabel("Municípios alcançados", color=COR_PRINCIPAL, fontweight="bold")
ax1.set_title("Evolução da Cobertura Territorial e Populacional\n(Rádio Alesc 2023–2026)", 
              fontweight="bold", fontsize=14, pad=25)

# Ajuste do limite Y1 para as etiquetas não baterem no teto do gráfico
ax1.set_ylim(0, cobertura_ano["Municipios_Alcancados"].max() * 1.25)

# 2. LABELS DAS BARRAS: Colocadas na base ou no topo com clareza
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height,
             f"{int(height)}", ha="center", va="bottom", 
             fontsize=11, fontweight="bold", color=COR_PRINCIPAL)

if "Pct_Pop_SC" in cobertura_ano.columns:
    # 3. SEGUNDO EIXO: Criamos a linha de evolução populacional
    ax2 = ax1.twinx()
    
    # 4. LINHA: Mais grossa e com cor de destaque (COR_ALERTA ou COR_SECUNDARIA)
    # A linha representa a "conquista humana", por isso deve estar em primeiro plano
    ax2.plot(x, cobertura_ano["Pct_Pop_SC"], marker="o", color=COR_ALERTA,
             linewidth=3, markersize=10, label="% pop. SC", zorder=5)
    
    ax2.set_ylabel("% da população de SC", color=COR_ALERTA, fontweight="bold")
    ax2.set_ylim(0, 100) # Importante: Fixar em 100% para dar noção de totalidade

    # 5. ANOTAÇÕES DA LINHA: Fundo branco (bbox) para evitar sobreposição com as barras
    for i, pct in enumerate(cobertura_ano["Pct_Pop_SC"]):
        ax2.annotate(f"{pct:.1f}%", (x[i], pct), 
                     xytext=(0, 12), textcoords="offset points", 
                     ha="center", fontsize=10, color=COR_ALERTA, 
                     fontweight="bold",
                     bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))

# Limpeza estética
ax1.grid(True, axis='y', linestyle='--', alpha=0.4)
ax2.grid(False) # Remove o grid do segundo eixo para não virar um "xadrez"

# Legenda unificada
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True)

fig.tight_layout()
salvar(fig, "02_cobertura_territorial_por_ano.png")

# ── 03 Série histórica mensal ─────────────────────────────────────────────────
""""
fig, ax = plt.subplots(figsize=(14, 5))
x = serie_mensal["AnoMes"].astype(str)
ax.plot(x, serie_mensal["Veiculacoes"], marker="o", color=COR_PRINCIPAL,
        linewidth=2, markersize=4)
ax.fill_between(range(len(x)), serie_mensal["Veiculacoes"], alpha=0.1, color=COR_PRINCIPAL)
media = serie_mensal["Veiculacoes"].mean()
ax.axhline(media, color="#888", linestyle="--", linewidth=1)
ax.text(len(x)-1, media+2, f"Média: {media:.0f}", fontsize=7, color="#888")
for idx, cor, lbl in [
    (serie_mensal["Veiculacoes"].idxmax(), COR_POSITIVO, "Pico"),
    (serie_mensal["Veiculacoes"].idxmin(), COR_ALERTA,   "Vale"),
]:
    ax.annotate(f"{lbl}: {serie_mensal.loc[idx,'Veiculacoes']}",
                xy=(idx, serie_mensal.loc[idx,"Veiculacoes"]),
                xytext=(0,14), textcoords="offset points",
                ha="center", fontsize=8, color=cor,
                arrowprops=dict(arrowstyle="-", color=cor, lw=1))
ax.set_title("Evolução Histórica de Veiculações Mensais — 2023–2026", fontweight="bold")
ax.set_ylabel("Veiculações")
plt.xticks(range(len(x)), x, rotation=60, ha="right", fontsize=7)
fig.tight_layout()
salvar(fig, "03_serie_historica_mensal.png")

# ── 04 Heatmap ano × mês ─────────────────────────────────────────────────────
pivot_hm = (
    df.groupby(["Ano","Mes"]).size().unstack(fill_value=0)
    .rename(columns={1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
                     7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"})
)
fig, ax = plt.subplots(figsize=(13, max(3, len(pivot_hm)*0.9)))
sns.heatmap(pivot_hm, annot=True, fmt="d", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"label":"Veiculações"})
ax.set_title("Heatmap de Veiculações por Ano e Mês — 2023–2026", fontweight="bold")
nota_rodape(ax, "Células frias em meses ativos = interrupção atípica")
fig.tight_layout()
salvar(fig, "04_heatmap_ano_mes.png")
"""
fig, ax = plt.subplots(figsize=(15, 6))
x_mes = serie_mensal["AnoMes"].astype(str)
y_mes = serie_mensal["Veiculacoes"]

# Linha de tendência (Média Móvel de 3 meses)
serie_mensal["Tendencia"] = y_mes.rolling(window=3, center=True).mean()

ax.plot(x_mes, y_mes, marker="o", color=COR_PRINCIPAL, alpha=0.3, label="Mensal")
ax.plot(x_mes, serie_mensal["Tendencia"], color=COR_PRINCIPAL, linewidth=3, label="Tendência")
ax.fill_between(range(len(x_mes)), y_mes, alpha=0.05, color=COR_PRINCIPAL)

# Destaques de Extremos
for idx, cor, lbl in [(y_mes.idxmax(), COR_POSITIVO, "PICO"), (y_mes.idxmin(), COR_ALERTA, "VALE")]:
    ax.annotate(f"{lbl}: {y_mes.loc[idx]}", xy=(idx, y_mes.loc[idx]),
                xytext=(0, 20), textcoords="offset points", ha="center", 
                fontsize=9, color="white", fontweight="bold",
                bbox=dict(boxstyle='round,pad=0.3', fc=cor, ec='none'))

ax.set_title("Evolução Mensal de Veiculações (Com Linha de Tendência)", fontweight="bold", fontsize=14)
n_step = 2 if len(x_mes) > 12 else 1
plt.xticks(range(0, len(x_mes), n_step), x_mes[::n_step], rotation=45, ha="right")
ax.set_ylim(0, y_mes.max() * 1.25)
ax.legend()
fig.tight_layout()
salvar(fig, "03_serie_historica_mensal.png")

# ── 05 Comparativo YoY ────────────────────────────────────────────────────────
yoy = df.groupby(["Ano","Mes"]).size().reset_index(name="Veiculacoes")
fig, ax = plt.subplots(figsize=(12, 5))
cores_anos = [COR_PRINCIPAL, COR_SECUNDARIA, COR_POSITIVO, COR_ALERTA]
for i, ano in enumerate(anos):
    d = yoy[yoy["Ano"]==ano].sort_values("Mes")
    ax.plot(d["Mes"], d["Veiculacoes"], marker="o", label=str(ano),
            color=cores_anos[i % len(cores_anos)], linewidth=2)
ax.set_xticks(range(1,13))
ax.set_xticklabels(["Jan","Fev","Mar","Abr","Mai","Jun",
                    "Jul","Ago","Set","Out","Nov","Dez"])
ax.set_ylabel("Veiculações")
ax.set_title("Comparativo Anual por Mês (Year-over-Year) — 2023–2026", fontweight="bold")
ax.legend(title="Ano")
fig.tight_layout()
salvar(fig, "05_comparativo_yoy.png")

# ── 06 Mix de conteúdo por ano ────────────────────────────────────────────────
'''
tipo_ano = (
    df.groupby(["Ano","Tipo"]).size().unstack(fill_value=0)
    .apply(lambda r: r/r.sum()*100, axis=1)
)
fig, ax = plt.subplots(figsize=(12, 6))
tipo_ano.plot(kind="bar", stacked=True, ax=ax, colormap="tab10", width=0.75)
ax.set_title("Evolução do Mix de Conteúdo por Ano (%) — 2023–2026", fontweight="bold")
ax.set_ylabel("Participação (%)")
ax.set_xticklabels([str(a) for a in tipo_ano.index], rotation=0)
ax.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.25,1))
fig.tight_layout()
salvar(fig, "06_mix_conteudo_por_ano.png")
'''
ordem_cats = (df.groupby("Tipo_Plot").size()
                .sort_values(ascending=False).index.tolist())
# Outros sempre por último
if "Outros" in ordem_cats:
    ordem_cats.remove("Outros")
    ordem_cats.append("Outros")
 
tipo_ano = (
    df.groupby(["Ano","Tipo_Plot"]).size()
    .unstack(fill_value=0)
    .reindex(columns=ordem_cats, fill_value=0)
    .apply(lambda r: r/r.sum()*100, axis=1)
)
 
fig, ax = plt.subplots(figsize=(13, 7), facecolor="#f8f9fa")
ax.set_facecolor("white")
x = range(len(anos_validos))
bottoms = {i: 0.0 for i in range(len(anos_validos))}
 
for cat in ordem_cats:
    if cat not in tipo_ano.columns: continue
    vals  = [tipo_ano.loc[ano, cat] if ano in tipo_ano.index else 0 for ano in anos_validos]
    color = PALETA_TIPO.get(cat, "#bdc3c7")
    ax.bar(x, vals, 0.55, bottom=[bottoms[i] for i in range(len(anos_validos))],
           color=color, label=cat, edgecolor="white", linewidth=0.5)
    for i, (v, bot) in enumerate(zip(vals, [bottoms[j] for j in range(len(anos_validos))])):
        if v >= 6.0:
            rgb = mcolors.to_rgb(color)
            lum = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
            ax.text(i, bot + v/2, f"{v:.0f}%", ha="center", va="center",
                    fontsize=8, fontweight="bold",
                    color="white" if lum < 0.5 else "#1a1a1a")
    for i, v in enumerate(vals):
        bottoms[i] += v
 
ax.set_xticks(x)
ax.set_xticklabels([str(a) for a in anos_validos], fontsize=12, fontweight="bold")
ax.set_ylabel("Participação (%)", fontsize=11)
ax.set_ylim(0, 108)
ax.set_title("Evolução do Mix de Conteúdo por Ano — Rádio Alesc (2023–2026)",
             fontsize=13, fontweight="bold", pad=12)
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
ax.spines[["top","right"]].set_visible(False)
totais = df.groupby("Ano").size()
for i, ano in enumerate(anos_validos):
    ax.text(i, -5, f"n={totais.get(ano,0):,}", ha="center", fontsize=9, color="#555")
handles = [mpatches.Patch(color=PALETA_TIPO.get(c,"#bdc3c7"), label=c)
           for c in ordem_cats if c in tipo_ano.columns]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=6, fontsize=8.5, framealpha=0.9, edgecolor="#ddd", fancybox=True)
nota_rodape(ax, "Especial, Legislação e Podcast consolidados em 'Outros'  |  2026 = jan–fev")
plt.tight_layout(rect=[0, 0.08, 1, 1])
salvar(fig, "06_mix_conteudo_por_ano.png")

# ── 07 Churn de rádios ────────────────────────────────────────────────────────
""""
if not df_churn.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(df_churn))
    ax.bar(x, df_churn["Entradas"], color=COR_POSITIVO, label="Novas rádios")
    ax.bar(x, df_churn["Saidas"],   color=COR_ALERTA,   label="Rádios que saíram")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(df_churn["Ano"])
    ax.set_ylabel("Número de rádios")
    ax.set_title("Churn Anual de Rádios Parceiras — 2023–2026", fontweight="bold")
    ax.legend()
    nota_rodape(ax, "Anos com muitas saídas indicam problema de retenção de parceiros")
    fig.tight_layout()
    salvar(fig, "07_churn_radios.png")
"""
fig, ax = plt.subplots(figsize=(12, 7))
x_labels = [str(a) for a in df_churn["Ano"]]

# Barras de Novas e Inativas (Garantindo que os nomes batam com o DataFrame acima)
ax.bar(x_labels, df_churn["Novas"], color=COR_POSITIVO, alpha=0.6, label="Novas Parceiras (Expansão)")
ax.bar(x_labels, df_churn["Saidas"], color=COR_ALERTA, alpha=0.6, label="Rádios Inativas no Ano")

# Linha de Base Ativa (Mostra o tamanho real da rede em cada ano)
ax.plot(x_labels, df_churn["Total_Ativas"], color="#333", marker="o", linewidth=2.5, 
        markersize=8, label="Total de Rádios Ativas")

# Adicionando os números sobre as barras para facilitar a leitura
for i, row in df_churn.iterrows():
    # Texto para Novas (Verde)
    ax.text(i, row["Novas"] + 1, f"+{int(row['Novas'])}", ha='center', 
            color=COR_POSITIVO, fontweight='bold', fontsize=10)
    # Texto para Inativas (Vermelho) - Só aparece se houver saídas
    if row["Saidas"] < 0:
        ax.text(i, row["Saidas"] - 4, f"{int(row['Saidas'])}", ha='center', 
                color=COR_ALERTA, fontweight='bold', fontsize=10)

# Estética do Gráfico
ax.axhline(0, color="black", linewidth=1) # Linha do horizonte
ax.set_title("Movimentação da Rede de Rádios Parceiras\n(Novas Conquistas vs. Inatividade)", 
             fontweight="bold", fontsize=14, pad=20)
ax.set_ylabel("Quantidade de Emissoras")
ax.set_ylim(df_churn["Saidas"].min() - 15, df_churn["Total_Ativas"].max() + 20)
ax.legend(loc="upper left", frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.3)

fig.tight_layout()
salvar(fig, "07_churn_radios.png")

# ── 08 Evolução individual das rádios ─────────────────────────────────────────
radios_multi = radio_ano.groupby("Radio")["Ano"].nunique()
top15 = (radio_ano[radio_ano["Radio"].isin(radios_multi[radios_multi>=2].index)]
         .groupby("Radio")["Veiculacoes"].sum().nlargest(15).index)
df_top = radio_ano[radio_ano["Radio"].isin(top15)]

fig, ax = plt.subplots(figsize=(14, 7))
cores_r = plt.cm.tab20(range(len(top15)))
for i, radio in enumerate(top15):
    d = df_top[df_top["Radio"]==radio].sort_values("Ano")
    ax.plot(d["Ano"], d["Veiculacoes"], marker="o", linewidth=2,
            markersize=5, color=cores_r[i], label=radio)
    ultimo = d.iloc[-1]
    ax.annotate(radio.split(" -")[0][:22], (ultimo["Ano"], ultimo["Veiculacoes"]),
                fontsize=6, xytext=(4,0), textcoords="offset points", color=cores_r[i])
ax.set_title("Evolução de Veiculações por Rádio — Top 15 (2023–2026)", fontweight="bold")
ax.set_ylabel("Veiculações por ano"); ax.set_xticks(anos)
ax.legend(fontsize=6.5, ncol=2, loc="upper left", framealpha=0.7)
nota_rodape(ax, "Linhas que chegam a zero = rádio saiu da rede")
fig.tight_layout()
salvar(fig, "08_evolucao_por_radio.png")

# ── 09 Fidelidade das rádios ──────────────────────────────────────────────────
top_fid = fidelidade.sort_values("Total_Veiculacoes", ascending=False).head(20)
cores_fid = [COR_POSITIVO if t==100 else COR_PRINCIPAL if t>=75 else COR_ALERTA
             for t in top_fid["Taxa_Fidelidade"]]
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_fid["Radio"][::-1], top_fid["Taxa_Fidelidade"][::-1],
               color=cores_fid[::-1])
ax.axvline(75, color="#888", linestyle="--", linewidth=1)
ax.set_xlabel("Taxa de fidelidade (%)")
ax.set_title("Fidelidade das Rádios Parceiras — Top 20", fontweight="bold")
ax.set_xlim(0, 120)
for bar, a in zip(bars, top_fid["Anos_Ativo"][::-1]):
    ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
            f"{int(a)} ano(s)", va="center", fontsize=7)
patches = [mpatches.Patch(color=COR_POSITIVO, label="100% — presença contínua"),
           mpatches.Patch(color=COR_PRINCIPAL, label="75–99% — parceira estável"),
           mpatches.Patch(color=COR_ALERTA,    label="<75% — parceira irregular")]
ax.legend(handles=patches, fontsize=8, loc="lower right")
nota_rodape(ax, "Rádios vermelhas merecem atenção de relacionamento")
fig.tight_layout()
salvar(fig, "09_fidelidade_radios.png")

# ── 10: Ranking de rádios por impacto ────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
top_imp = impacto_radio.head(15)
ax.barh(top_imp["Radio"][::-1], top_imp["Impacto"][::-1]/1e6, color=COR_SECUNDARIA)
ax.set_xlabel("Impacto acumulado (veiculações × pop. — M)")
ax.set_title("Top 15 Rádios por Impacto Real* — Histórico Total", fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.1f}M"))
nota_rodape(ax, "*Impacto = veiculações × população do município. "
                "Distingue rádios em cidades grandes de rádios em cidades pequenas.")
fig.tight_layout()
salvar(fig, "10_ranking_radios_por_impacto.png")

# ── 11 Gini + lacunas ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
# Lorenz
ax = axes[0]
v = sorted(alcance["Veiculacoes"].tolist())
n = len(v); s = sum(v)
lx = [i/n for i in range(n+1)]
ly = [0] + [sum(v[:i+1])/s for i in range(n)]
ax.plot(lx, ly, color=COR_PRINCIPAL, linewidth=2, label="Rádio Alesc")
ax.plot([0,1],[0,1], "--", color="#888", linewidth=1, label="Distribuição perfeita")
ax.fill_between(lx, ly, lx, alpha=0.15, color=COR_PRINCIPAL)
ax.set_title(f"Curva de Lorenz — Cobertura Territorial\nGini = {gini_val:.3f}",
             fontweight="bold")
ax.set_xlabel("Proporção de municípios"); ax.set_ylabel("Proporção de veiculações")
ax.legend()
interp = ("distribuída" if gini_val < 0.4 else
          "moderadamente concentrada" if gini_val < 0.6 else "fortemente concentrada")
nota_rodape(ax, f"Cobertura {interp}")
# Lacunas
ax = axes[1]
if not lacunas.empty:
    ax.barh(lacunas["Municipio_IBGE"][::-1], lacunas["Populacao"][::-1]/1000,
            color=COR_ALERTA)
    ax.set_xlabel("População (mil habitantes)")
    ax.set_title(f"Lacunas Estratégicas\nCidades >{LIMIAR_LACUNA//1000}k hab. sem cobertura",
                 fontweight="bold")
    nota_rodape(ax, "Cada cidade = oportunidade de expansão de parceria")
else:
    ax.text(0.5, 0.5, "Sem lacunas\nacima de 50k hab.",
            ha="center", va="center", transform=ax.transAxes, fontsize=12)
    ax.set_title("Lacunas Estratégicas", fontweight="bold")
fig.tight_layout()
salvar(fig, "11_gini_e_lacunas.png")

# ── 12 Municípios por mês ─────────────────────────────────────────────────────
mun_mes = df.groupby("AnoMes")["Cidade"].nunique().reset_index(name="Municipios")
fig, ax = plt.subplots(figsize=(14, 5))
x = mun_mes["AnoMes"].astype(str)
ax.plot(x, mun_mes["Municipios"], marker="o", color=COR_SECUNDARIA,
        linewidth=2, markersize=4)
ax.fill_between(range(len(x)), mun_mes["Municipios"], alpha=0.1, color=COR_SECUNDARIA)
ax.axhline(mun_mes["Municipios"].mean(), color="#888", linestyle="--", linewidth=1)
ax.set_title("Municípios Alcançados por Mês — 2023–2026", fontweight="bold")
ax.set_ylabel("Municípios únicos")
plt.xticks(range(len(x)), x, rotation=60, ha="right", fontsize=7)
fig.tight_layout()
salvar(fig, "12_municipios_por_mes.png")

# ── 13 Perfil de conteúdo por rádio ──────────────────────────────────────────
top_r_idx = df["Radio"].value_counts().head(TOP_N_RADIOS).index
pivot_p = (df[df["Radio"].isin(top_r_idx)]
           .groupby(["Radio","Tipo"]).size().unstack(fill_value=0))
fig, ax = plt.subplots(figsize=(14, 6))
pivot_p.plot(kind="bar", ax=ax, colormap="tab10", width=0.8)
ax.set_ylabel("Veiculações")
ax.set_title("Perfil de Conteúdo por Rádio (Top 10) — Histórico Total", fontweight="bold")
plt.xticks(rotation=35, ha="right", fontsize=8)
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
salvar(fig, "13_perfil_conteudo_por_radio.png")

# Gráfico 14: Ciclo de vida médio por tipo
fig, ax = plt.subplots(figsize=(12, 6))
ciclo_tipo_plot = ciclo_tipo[ciclo_tipo["Veiculacoes"] >= 10]
ax.barh(ciclo_tipo_plot["Tipo"][::-1], 
        ciclo_tipo_plot["Mediana_dias"][::-1], 
        color=COR_PRINCIPAL)
ax.set_xlabel("Mediana de dias entre criação e veiculação")
ax.set_title("Ciclo de Vida Mediano por Tipo de Conteúdo", fontweight="bold")
nota_rodape(ax, "Tipos com mediana alta = conteúdo evergreen ou distribuição lenta")
fig.tight_layout()
salvar(fig, "14_ciclo_vida_por_tipo.png")

# Gráfico 15: Distribuição de quando as veiculações ocorrem (dias 0–30)
fig, ax = plt.subplots(figsize=(12, 5))
dados_hist = df_ciclo[df_ciclo["Dias_Ate_Veiculacao"] <= 30]["Dias_Ate_Veiculacao"]
ax.hist(dados_hist, bins=31, range=(0, 30), 
        color=COR_SECUNDARIA, edgecolor="white")
ax.set_xlabel("Dias após a criação")
ax.set_ylabel("Número de veiculações")
ax.set_title("Quando os Conteúdos São Veiculados Após a Criação (primeiros 30 dias)",
             fontweight="bold")
pct_d0 = (dados_hist == 0).mean() * 100
pct_d3 = (dados_hist <= 3).mean() * 100
nota_rodape(ax, f"Dia 0: {pct_d0:.0f}% | Primeiros 3 dias: {pct_d3:.0f}% das veiculações")
fig.tight_layout()
salvar(fig, "15_janela_veiculacao.png")

#
# 5.1 NOVO: MAPA INTERATIVO (PLOTLY)
# ══════════════════════════════════════════════════════════════════════════════
import plotly.express as px

print("\n[4.1/8] Gerando Mapa Interativo Digital...")

# Garantir que temos dados para plotar
if not mapa_df.empty:
    fig_interativo = px.scatter_mapbox(
        mapa_df,
        lat="lat",
        lon="lon",
        size="Populacao",           # O tamanho da bolha indica a relevância da cidade
        color="Veiculacoes",        # A cor indica a intensidade do trabalho (esforço)
        hover_name="Cidade",        # Nome da cidade aparece no topo do balão
        hover_data={
            "lat": False, 
            "lon": False,
            "Veiculacoes": ":,",    # Formata com separador de milhar
            "Audiencia_Unica": ":.0f",
            "Populacao": ":.0f"
        },
        # Escala de cores profissional (amarelo para roxo escuro)
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=40,               
        zoom=6.8,                   # Enquadramento focado em Santa Catarina
        mapbox_style="carto-positron", # Estilo limpo com cidades e rodovias ao fundo
        title=f"Painel Interativo de Cobertura Rádio ALESC ({anos[0]}-{anos[-1]})",
        labels={
            "Veiculacoes": "Inserções", 
            "Audiencia_Unica": "Impacto Estimado (Pessoas)",
            "Populacao": "População Total"
        }
    )

    # Ajustes finos de layout
    fig_interativo.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        paper_bgcolor="#f8f9fa"
    )

    # Salvando o arquivo HTML
    caminho_interativo = OUTPUT_DIR / "mapa_interativo_alesc.html"
    fig_interativo.write_html(str(caminho_interativo))
    print(f"  ✓ {caminho_interativo.name} gerado com sucesso.")
else:
    print("  ⚠ Erro: mapa_df está vazio. Verifique os centroides.")

# ══════════════════════════════════════════════════════════════════════════════
# 6. EXPORTAÇÕES (CONTINUAÇÃO DO SEU CÓDIGO)
# ══════════════════════════════════════════════════════════════════════════════

ciclo_tipo.to_csv(OUTPUT_DIR / "ciclo_vida_por_tipo.csv", index=False)
ciclo_comercial.head(50).to_csv(OUTPUT_DIR / "comerciais_mais_longevos.csv", index=False)
zumbis.head(30).to_csv(OUTPUT_DIR / "conteudos_zumbis.csv", index=False)

# ══════════════════════════════════════════════════════════════════════════════
# 6. EXPORTAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
print("\n[5/8] Exportando tabelas...")

df_export = df.drop(columns=["Arquivo","Hora_dt","Cidade_norm"], errors="ignore")
df_export.to_csv(OUTPUT_DIR / "dataset_consolidado.csv", index=False, encoding="utf-8-sig")
print("  ✓ dataset_consolidado.csv")

alcance.drop(columns=["Cidade_norm"], errors="ignore").sort_values(
    "Alcance_Ponderado", ascending=False
).to_excel(OUTPUT_DIR / "alcance_municipios.xlsx", index=False)
print("  ✓ alcance_municipios.xlsx")

# Export dedicado do Índice de Intensidade — ordenado do mais para o menos intenso
(alcance[["Cidade","Populacao","Veiculacoes","Indice_Intensidade","Alcance_Ponderado"]]
 .drop_duplicates()
 .sort_values("Indice_Intensidade", ascending=False)
 .to_csv(OUTPUT_DIR / "intensidade_por_municipio.csv", index=False, encoding="utf-8-sig"))
print("  ✓ intensidade_por_municipio.csv")

fidelidade.sort_values("Taxa_Fidelidade", ascending=False).to_excel(
    OUTPUT_DIR / "fidelidade_radios.xlsx", index=False)
print("  ✓ fidelidade_radios.xlsx")

impacto_radio.head(30).to_csv(OUTPUT_DIR / "impacto_por_radio.csv", index=False)
print("  ✓ impacto_por_radio.csv")

cobertura_ano.to_csv(OUTPUT_DIR / "cobertura_por_ano.csv", index=False)
print("  ✓ cobertura_por_ano.csv")

serie_mensal.to_csv(OUTPUT_DIR / "serie_mensal.csv", index=False)
print("  ✓ serie_mensal.csv")

if not lacunas.empty:
    lacunas.to_csv(OUTPUT_DIR / "lacunas_estrategicas.csv", index=False)
    print("  ✓ lacunas_estrategicas.csv")

if not df_churn.empty:
    df_churn.to_csv(OUTPUT_DIR / "churn_radios.csv", index=False)
    print("  ✓ churn_radios.csv")

df_val.to_csv(OUTPUT_DIR / "00_relatorio_validacao.csv", index=False)
print("  ✓ 00_relatorio_validacao.csv")

# Garante que apenas anos válidos são processados (remove fantasmas como 1970)
anos_validos = [a for a in anos if a >= 2020]

# ── Função segura para acessar resumo por ano/coluna ─────────────────────────
# Evita IndexError quando ano não tem linha para aquele status (bug apontado)
def safe_get(df_resumo, ano, col):
    linha = df_resumo[df_resumo["Ano"] == ano]
    if linha.empty or col not in linha.columns:
        return 0
    vals = linha[col].values
    return int(vals[0]) if len(vals) > 0 else 0

# ── Radio_norm: normalizado SÓ para comparação, não altera nome exibido ───────
# Evita falsos "novos/saiu" por variação de grafia ("Rádio X" vs "Radio X")
df["Radio_norm"] = (df["Radio"].str.strip()
                               .str.lower()
                               .str.replace(r'\s+', ' ', regex=True))

# Anos válidos — sorted() explícito para blindar contra reordenação acidental
anos_validos = sorted([a for a in anos if a >= 2020])

# ── RELATÓRIO 1: Municípios perdidos por ano ──────────────────────────────────
# Para cada transição entre anos, lista os municípios que saíram da cobertura.
# "Perdido" = estava no ano anterior, não aparece no ano atual.
 
linhas_mun = []
for i in range(1, len(anos_validos)):
    a_ant, a_cur = anos_validos[i-1], anos_validos[i]
    cids_ant = set(df[df["Ano"] == a_ant]["Cidade_norm"].dropna().unique())
    cids_cur = set(df[df["Ano"] == a_cur]["Cidade_norm"].dropna().unique())

    perdidos_norm = sorted(cids_ant - cids_cur)
    novos_norm    = sorted(cids_cur - cids_ant)

    # Mapa norm → nome original para exibição
    mapa_ant = (df[df["Ano"] == a_ant].drop_duplicates("Cidade_norm")
                .set_index("Cidade_norm")["Cidade"].to_dict())
    mapa_cur = (df[df["Ano"] == a_cur].drop_duplicates("Cidade_norm")
                .set_index("Cidade_norm")["Cidade"].to_dict())

    for cn in perdidos_norm:
        if cn:  # ignora string vazia
            linhas_mun.append({
                "Transicao":      f"{a_ant}→{a_cur}",
                "Ano_Referencia": a_cur,
                "Municipio":      mapa_ant.get(cn, cn),
                "Status":         "Perdido",
            })
    for cn in novos_norm:
        if cn:
            linhas_mun.append({
                "Transicao":      f"{a_ant}→{a_cur}",
                "Ano_Referencia": a_cur,
                "Municipio":      mapa_cur.get(cn, cn),
                "Status":         "Novo",
            })

df_municipios_movimento = pd.DataFrame(linhas_mun)

resumo_mun = (df_municipios_movimento
              .groupby(["Transicao","Status"]).size()
              .unstack(fill_value=0).reset_index())

df_municipios_movimento.to_csv(
    OUTPUT_DIR / "relatorio_municipios_movimento.csv",
    index=False, encoding="utf-8-sig"
)
print("  ✓ relatorio_municipios_movimento.csv")
print(f"    {'Transição':<12} {'Perdidos':>10} {'Novos':>8} {'Saldo':>8}")
print(f"    {'-'*42}")
for _, row in resumo_mun.iterrows():
    perdidos = int(row.get("Perdido", 0))
    novos    = int(row.get("Novo", 0))
    saldo    = novos - perdidos
    sinal    = "+" if saldo >= 0 else ""
    print(f"    {row['Transicao']:<12} {perdidos:>10} {novos:>8} {sinal+str(saldo):>8}")
 
 
# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO 2: Rádios — entradas, saídas e retenção por ano
# ══════════════════════════════════════════════════════════════════════════════
# Usa Radio_norm para comparação
# Status:
#   "Nova"       = nunca apareceu antes no histórico
#   "Retornou"   = já existia, ficou ausente em algum ano, voltou
#   "Saiu"       = estava no ano anterior, não aparece no atual (inativa no ano)
#   "Persistente"= estava no ano anterior e continua ativa
# Taxa de retenção = Persistentes / Total do ano anterior

historico_radios_norm = set()
linhas_rad = []

for i, ano in enumerate(anos_validos):
    rads_norm_ano = set(df[df["Ano"] == ano]["Radio_norm"].dropna().unique())
    # Mapa norm → nome original para exibição
    mapa_radio = (df[df["Ano"] == ano].drop_duplicates("Radio_norm")
                  .set_index("Radio_norm")["Radio"].to_dict())

    if i == 0:
        for rn in sorted(rads_norm_ano):
            linhas_rad.append({
                "Ano": ano, "Radio": mapa_radio.get(rn, rn),
                "Status": "Ativa (ano base)"
            })
        historico_radios_norm.update(rads_norm_ano)
        continue

    a_ant = anos_validos[i-1]
    rads_norm_ant = set(df[df["Ano"] == a_ant]["Radio_norm"].dropna().unique())

    saiu        = sorted(rads_norm_ant - rads_norm_ano)
    novas       = sorted(rads_norm_ano - historico_radios_norm)
    retornou    = sorted((rads_norm_ano - rads_norm_ant) & historico_radios_norm)
    persistente = sorted(rads_norm_ano & rads_norm_ant)

    mapa_ant = (df[df["Ano"] == a_ant].drop_duplicates("Radio_norm")
                .set_index("Radio_norm")["Radio"].to_dict())

    for rn in saiu:
        linhas_rad.append({"Ano": ano, "Radio": mapa_ant.get(rn, rn), "Status": "Saiu"})
    for rn in novas:
        linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn, rn), "Status": "Nova"})
    for rn in retornou:
        linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn, rn), "Status": "Retornou"})
    for rn in persistente:
        linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn, rn), "Status": "Persistente"})

    historico_radios_norm.update(rads_norm_ano)

df_radios_movimento = pd.DataFrame(linhas_rad)

resumo_rad = (df_radios_movimento[df_radios_movimento["Status"] != "Ativa (ano base)"]
              .groupby(["Ano","Status"]).size()
              .unstack(fill_value=0).reset_index())

df_radios_movimento.to_csv(
    OUTPUT_DIR / "relatorio_radios_movimento.csv",
    index=False, encoding="utf-8-sig"
)
print("  ✓ relatorio_radios_movimento.csv")
print(f"    {'Ano':<8} {'Saíram':>8} {'Novas':>8} {'Retorn.':>9} {'Persist.':>10} {'Retenção':>10} {'Ativas':>8}")
print(f"    {'-'*65}")
for ano in anos_validos[1:]:
    saiu_n   = safe_get(resumo_rad, ano, "Saiu")
    nova_n   = safe_get(resumo_rad, ano, "Nova")
    ret_n    = safe_get(resumo_rad, ano, "Retornou")
    pers_n   = safe_get(resumo_rad, ano, "Persistente")
    ativas   = df[df["Ano"] == ano]["Radio"].nunique()
    a_ant    = anos_validos[anos_validos.index(ano) - 1]
    ant_tot  = df[df["Ano"] == a_ant]["Radio"].nunique()
    retencao = f"{pers_n/ant_tot*100:.1f}%" if ant_tot > 0 else "—"
    print(f"    {ano:<8} {saiu_n:>8} {nova_n:>8} {ret_n:>9} {pers_n:>10} {retencao:>10} {ativas:>8}")

 
""""
# ── RELATÓRIO 3: Somatório da população dos municípios cobertos por ano ───────
# Usa a tabela df_pop (IBGE) para somar a população dos municípios que
# tiveram pelo menos 1 veiculação no ano — sem duplicar por veiculação.
 
linhas_pop = []
for ano in anos_validos:
    cids_ano  = set(df[df["Ano"] == ano]["Cidade_norm"].dropna().unique())
    n_cids    = len(cids_ano)
 
    if df_pop is not None:
        pop_total_ano = df_pop[df_pop["Cidade_norm"].isin(cids_ano)]["Populacao"].sum()
        pct_sc        = pop_total_ano / POP_SC_TOTAL * 100
    else:
        pop_total_ano = n_cids * 12_000  # fallback aproximado
        pct_sc        = pop_total_ano / POP_SC_TOTAL * 100
 
    linhas_pop.append({
        "Ano":                  ano,
        "Municipios_Cobertos":  n_cids,
        "Pop_Coberta":          int(pop_total_ano),
        "Pct_Pop_SC":           round(pct_sc, 2),
        "Pop_SC_Total":         POP_SC_TOTAL,
    })
 
df_pop_ano = pd.DataFrame(linhas_pop)
 
df_pop_ano.to_csv(
    OUTPUT_DIR / "relatorio_populacao_por_ano.csv",
    index=False, encoding="utf-8-sig"
)
print("  ✓ relatorio_populacao_por_ano.csv")
print(f"    {'Ano':<8} {'Municípios':>12} {'Pop. Coberta':>14} {'% SC':>8}")
print(f"    {'-'*46}")
for _, row in df_pop_ano.iterrows():
    print(f"    {int(row['Ano']):<8} {int(row['Municipios_Cobertos']):>12} "
          f"{int(row['Pop_Coberta']):>14,} {row['Pct_Pop_SC']:>7.1f}%")
 
# ── Adiciona seção ao relatório analítico ────────────────────────────────────
secao_extra = [
    "",
    "── DINÂMICA DE COBERTURA ────────────────────────────────────",
]
 
# Municípios
secao_extra.append("  Municípios: entradas e saídas por ano")
for _, row in resumo_mun.iterrows():
    perdidos = int(row.get("Perdido", 0))
    novos    = int(row.get("Novo", 0))
    saldo    = novos - perdidos
    sinal    = "+" if saldo >= 0 else ""
    secao_extra.append(
        f"    {row['Transicao']}: -{perdidos} municípios saíram, "
        f"+{novos} entraram (saldo {sinal}{saldo})"
    )
 
secao_extra.append("")
secao_extra.append("  Rádios: movimentação por ano")
for ano in anos_validos[1:]:
    saiu   = int(resumo_rad.loc[resumo_rad["Ano"]==ano, "Saiu"].values[0])     if "Saiu"     in resumo_rad.columns else 0
    nova   = int(resumo_rad.loc[resumo_rad["Ano"]==ano, "Nova"].values[0])     if "Nova"     in resumo_rad.columns else 0
    ret    = int(resumo_rad.loc[resumo_rad["Ano"]==ano, "Retornou"].values[0]) if "Retornou" in resumo_rad.columns else 0
    ativas = df[df["Ano"]==ano]["Radio"].nunique()
    secao_extra.append(
        f"    {ano}: {saiu} saíram | {nova} novas | {ret} retornaram "
        f"→ {ativas} ativas"
    )
 
secao_extra.append("")
secao_extra.append("  População coberta por ano (municípios únicos × pop. IBGE 2021)")
for _, row in df_pop_ano.iterrows():
    secao_extra.append(
        f"    {int(row['Ano'])}: {int(row['Municipios_Cobertos'])} municípios — "
        f"{int(row['Pop_Coberta']):,} hab. ({row['Pct_Pop_SC']:.1f}% de SC)"
    )
 
# Imprime seção extra no terminal
print()
print("\n".join(secao_extra))
 
# Salva versão estendida do relatório
relatorio_estendido = relatorio_txt.replace(
    "=" * 65 + "\n",
    "=" * 65 + "\n" + "\n".join(secao_extra) + "\n",
    1  # substitui só a primeira ocorrência (rodapé)
)
# Na verdade anexa antes do último separador
linhas_rel = relatorio_txt.split("\n")
idx_fim = next(i for i in range(len(linhas_rel)-1, -1, -1)
               if linhas_rel[i].startswith("="))
linhas_rel = linhas_rel[:idx_fim] + secao_extra + ["", "=" * 65]
(OUTPUT_DIR / "relatorio_analitico.txt").write_text(
    "\n".join(linhas_rel), encoding="utf-8"
)
print("\n  ✓ relatorio_analitico.txt atualizado com seção de dinâmica")
"""
# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO 3: Somatório da população coberta por ano
# ══════════════════════════════════════════════════════════════════════════════
# Soma a população IBGE de cada município que teve ≥1 veiculação no ano
# Cada município conta UMA vez independente de quantas veiculações teve

linhas_pop = []
for ano in anos_validos:
    cids_ano = set(df[df["Ano"] == ano]["Cidade_norm"].dropna().unique())
    n_cids   = len([c for c in cids_ano if c])  # ignora string vazia

    if df_pop is not None:
        pop_coberta = df_pop[df_pop["Cidade_norm"].isin(cids_ano)]["Populacao"].sum()
    else:
        pop_coberta = n_cids * 12_000  # fallback aproximado

    pct_sc = pop_coberta / POP_SC_TOTAL * 100

    linhas_pop.append({
        "Ano":                 ano,
        "Municipios_Cobertos": n_cids,
        "Pop_Coberta":         int(pop_coberta),
        "Pct_Pop_SC":          round(pct_sc, 2),
        "Audiencia_Potencial": int(pop_coberta * TAXA_ESCUTA_RADIO),
        "Pct_Audiencia_SC":    round(pop_coberta * TAXA_ESCUTA_RADIO / POP_SC_TOTAL * 100, 2),
        "Pop_SC_Total":        POP_SC_TOTAL,
        "Pop_Nao_Coberta":     POP_SC_TOTAL - int(pop_coberta),
    })

df_pop_ano = pd.DataFrame(linhas_pop)

df_pop_ano.to_csv(
    OUTPUT_DIR / "relatorio_populacao_por_ano.csv",
    index=False, encoding="utf-8-sig"
)
print("  ✓ relatorio_populacao_por_ano.csv")
print(f"    {'Ano':<8} {'Municípios':>12} {'Pop. Coberta':>14} {'% SC':>8} {'Pop. Fora':>14}")
print(f"    {'-'*60}")
for _, row in df_pop_ano.iterrows():
    print(f"    {int(row['Ano']):<8} {int(row['Municipios_Cobertos']):>12} "
          f"{int(row['Pop_Coberta']):>14,} {row['Pct_Pop_SC']:>7.1f}% "
          f"{int(row['Pop_Nao_Coberta']):>14,}")

# ── Seção extra no relatório analítico ───────────────────────────────────────
secao_extra = [
    "",
    "── DINÂMICA DE COBERTURA ────────────────────────────────────",
    "  Municípios: entradas e saídas por transição de ano",
]
for _, row in resumo_mun.iterrows():
    perdidos = int(row.get("Perdido", 0))
    novos    = int(row.get("Novo", 0))
    saldo    = novos - perdidos
    sinal    = "+" if saldo >= 0 else ""
    secao_extra.append(
        f"    {row['Transicao']}: -{perdidos} perdidos, +{novos} novos "
        f"(saldo {sinal}{saldo})"
    )

secao_extra.append("")
secao_extra.append("  Rádios: movimentação e taxa de retenção por ano")
for ano in anos_validos[1:]:
    saiu_n   = safe_get(resumo_rad, ano, "Saiu")
    nova_n   = safe_get(resumo_rad, ano, "Nova")
    ret_n    = safe_get(resumo_rad, ano, "Retornou")
    pers_n   = safe_get(resumo_rad, ano, "Persistente")
    ativas   = df[df["Ano"] == ano]["Radio"].nunique()
    a_ant    = anos_validos[anos_validos.index(ano) - 1]
    ant_tot  = df[df["Ano"] == a_ant]["Radio"].nunique()
    retencao = f"{pers_n/ant_tot*100:.1f}%" if ant_tot > 0 else "—"
    secao_extra.append(
        f"    {ano}: {saiu_n} saíram | {nova_n} novas | {ret_n} retornaram | "
        f"{pers_n} persistentes | retenção {retencao} | {ativas} ativas"
    )

secao_extra.append("")
secao_extra.append("  População coberta por ano (municípios únicos × pop. IBGE 2021)")
for _, row in df_pop_ano.iterrows():
    secao_extra.append(
        f"    {int(row['Ano'])}: {int(row['Municipios_Cobertos'])} municípios — "
        f"{int(row['Pop_Coberta']):,} hab. ({row['Pct_Pop_SC']:.1f}% de SC)"
    )

# Imprime no terminal
print()
for l in secao_extra:
    print(l)

""""
# Atualiza relatorio_analitico.txt
try:
    linhas_rel = relatorio_txt.split("\n")
    idx_fim = next(i for i in range(len(linhas_rel)-1, -1, -1)
                   if linhas_rel[i].startswith("="))
    linhas_rel = linhas_rel[:idx_fim] + secao_extra + ["", "=" * 65]
    (OUTPUT_DIR / "relatorio_analitico.txt").write_text(
        "\n".join(linhas_rel), encoding="utf-8"
    )
    print("\n  ✓ relatorio_analitico.txt atualizado com seção DINÂMICA DE COBERTURA")
except Exception as e:
    print(f"  ⚠ Não foi possível atualizar relatorio_analitico.txt: {e}")
"""
# ══════════════════════════════════════════════════════════════════════════════
# 7. RELATÓRIO ANALÍTICO EM TEXTO
# ══════════════════════════════════════════════════════════════════════════════
print("\n[6/8] Gerando relatório analítico...")

linhas = [
    "=" * 65,
    "RELATÓRIO ANALÍTICO — RÁDIO ALESC",
    f"Período: {df['Data'].min().date()} → {df['Data'].max().date()}",
    "=" * 65,
    "",
    "── VISÃO GERAL ──────────────────────────────────────────────",
    f"Total de veiculações:       {len(df):,}",
]
for ano in anos:
    linhas.append(f"  {ano}: {(df['Ano']==ano).sum():,} veiculações")
linhas += [
    f"Rádios parceiras ativas:    {df['Radio'].nunique()}",
    f"Municípios alcançados:      {df['Cidade'].nunique()} de 295 em SC",
    f"Tipo mais veiculado:        {tipo_count.idxmax()} ({tipo_count.max():,})",
    "",
    "── COBERTURA TERRITORIAL ────────────────────────────────────",
]
for _, row in cobertura_ano.iterrows():
    linha = f"  {int(row['Ano'])}: {int(row['Municipios_Alcancados'])} municípios"
    if "Pct_Pop_SC" in row:
        linha += f" — {row['Pct_Pop_SC']:.1f}% da população de SC"
    linhas.append(linha)

if df_pop is not None and "tem_cobertura" in df_pop.columns:
    pop_coberta = df_pop[df_pop["tem_cobertura"]]["Populacao"].sum()
    linhas.append(f"\n  Cobertura acumulada (histórico): "
                  f"{pop_coberta/POP_SC_TOTAL*100:.1f}% da população de SC")

linhas += [
    "",
    "── ÍNDICE DE GINI TERRITORIAL ───────────────────────────────",
    f"  Gini = {gini_val:.3f}",
    f"  Interpretação: cobertura {'distribuída' if gini_val<0.4 else 'moderadamente concentrada' if gini_val<0.6 else 'fortemente concentrada'}",
    "",
    "── REDE DE PARCEIROS ────────────────────────────────────────",
]
top10_exec = df["Radio"].value_counts().head(10).sum()
linhas.append(f"  Concentração top 10 rádios: {top10_exec/len(df)*100:.1f}% das veiculações")

if not fidelidade.empty:
    continuas = ((fidelidade["Taxa_Fidelidade"] == 100) & 
             (fidelidade["Anos_Ativo"] >= 2)).sum()
    irregulares = ((fidelidade["Taxa_Fidelidade"] < 75) & 
               (fidelidade["Anos_Ativo"] >= 2)).sum()
    linhas += [
        f"  Rádios com presença contínua (100%):   {continuas}",
        f"  Rádios com presença irregular (<75%):  {irregulares}",
    ]

if not df_churn.empty:
    ano_mais_perdas = df_churn.loc[df_churn["Saidas"].idxmin(), "Ano"]
    linhas.append(f"  Ano com mais saídas de parceiros: {ano_mais_perdas}")

if not lacunas.empty:
    linhas += [
        "",
        f"── LACUNAS ESTRATÉGICAS ({len(lacunas)} cidades >{LIMIAR_LACUNA//1000}k hab.) ──",
    ]
    for _, row in lacunas.head(8).iterrows():
        linhas.append(f"  → {row['Municipio_IBGE']}: {row['Populacao']:,} hab.")

# ── ÍNDICE DE INTENSIDADE ─────────────────────────────────────────────────────
# Veiculações por 10.000 habitantes — distingue cidades pequenas saturadas
# de cidades grandes subatendidas
intensidade = alcance[["Cidade","Populacao","Veiculacoes","Indice_Intensidade"]].copy()
intensidade = intensidade[intensidade["Populacao"] > 0].copy()
 
top_intens    = intensidade.nlargest(8, "Indice_Intensidade")
bottom_intens = (intensidade[intensidade["Veiculacoes"] >= 5]  # mín. 5 veic. para relevância
                 .nsmallest(8, "Indice_Intensidade"))
 
linhas += [
    "",
    "── ÍNDICE DE INTENSIDADE (veiculações/10k hab.) ─────────────",
    "  Municípios com MAIOR intensidade (possível saturação):",
]
for _, row in top_intens.iterrows():
    linhas.append(
        f"    {row['Cidade']:<30} {row['Indice_Intensidade']:>8.1f} "
        f"({int(row['Veiculacoes'])} veic. / {int(row['Populacao']):,} hab.)"
    )
linhas += ["", "  Municípios com MENOR intensidade (potencial subatendido):"]
for _, row in bottom_intens.iterrows():
    linhas.append(
        f"    {row['Cidade']:<30} {row['Indice_Intensidade']:>8.1f} "
        f"({int(row['Veiculacoes'])} veic. / {int(row['Populacao']):,} hab.)"
    )

linhas += [
    "",
    "── FRASES PRONTAS PARA APRESENTAÇÃO ────────────────────────",
    f"  'A Rádio Alesc distribuiu {len(df):,} veiculações entre {anos[0]} e {anos[-1]},'",
    f"  'alcançando {df['Cidade'].nunique()} municípios catarinenses.'",
]
if "Pct_Pop_SC" in cobertura_ano.columns:
    ult = cobertura_ano.iloc[-1]
    linhas.append(
        f"  'Em {int(ult['Ano'])}, a programação alcançou municípios onde vivem "
        f"{ult['Pct_Pop_SC']:.1f}% dos catarinenses.'"
    )
if not lacunas.empty:
    linhas.append(
        f"  'Há {len(lacunas)} cidades com mais de {LIMIAR_LACUNA//1000} mil habitantes ainda sem "
        "cobertura — oportunidade concreta de expansão.'"
    )
linhas += ["", "=" * 65]

relatorio_txt = "\n".join(linhas)
(OUTPUT_DIR / "relatorio_analitico.txt").write_text(relatorio_txt, encoding="utf-8")
print("  ✓ relatorio_analitico.txt")
print()
print(relatorio_txt)

# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMÁRIO FINAL
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n[7/8] Concluído.")
print(f"  Gráficos: 15 | Tabelas: 9 | Relatório: relatorio_analitico.txt")
print(f"  Cache IBGE: {CACHE_DIR}/")
print(f"  Outputs:    {OUTPUT_DIR}/\n")

