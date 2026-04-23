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
from io import StringIO
from pathlib import Path

# warnings.filterwarnings("ignore")

DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / "cache"
OUTPUT_DIR = Path("outputs")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

TAXA_ESCUTA_RADIO = 0.80 # Pesquisa ACAERT oito em cada dez catarinenses ouvem rádio - Dados de 2024
LIMIAR_LACUNA = 20.000 # Para clareza nos gráficos, considera municípios com mais de 20.000 habitantes
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
        # Frentes Parlamentares
        "FP":           "Frente Parlamentar",
        "FRENTE":       "Frente Parlamentar",
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
        # Legislação sancionada / executivo
        "SANCIONADOS":  "Legislação Sancionada",
        "SANÇÃO":       "Legislação Sancionada",
        "VETO":         "Veto",
        "DECRETO":      "Decreto",
        # Informativo / institucional
        "INFORMATIVO":  "Informativo",
        "INSTITUCIONAL":"Institucional",
        "CHAMADA":      "Institucional",
        # Outros tipos mapeáveis
        "PLE":          "Pronunciamento",
        "RF":           "Redação Final",
        "BANCADA":      "Bancada",
        "MOÇÃO":        "Moção",
        "MOCAO":        "Moção",
        "ESPECIAL":     "Especial",
        "LIVRO":        "Livro",
        "PRES":         "Presidência",
        "SUSP":         "Suspensão",
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

        tmp.columns = COLUNAS_7[:len(tmp.columns)]
        tmp["Veiculacoes"] = 1

        # Remove linhas completamente vazias
        tmp = tmp.dropna(subset=[tmp.columns[0]])

        datas = pd.to_datetime(tmp["Data"], dayfirst=True, errors="coerce")
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
        relatorio_val.append({"Arquivo": arq.name, "Registros": 0,
                               "Status": f"ERRO: {e}"})

df_val = pd.DataFrame(relatorio_val)
print(df_val[["Arquivo","Registros","Separador","Status"]].to_string(index=False))
df_val.to_csv(OUTPUT_DIR / "00_relatorio_validacao.csv", index=False)

# ══════════════════════════════════════════════════════════════════════════════
# 2. CONSOLIDAÇÃO E LIMPEZA
# ══════════════════════════════════════════════════════════════════════════════