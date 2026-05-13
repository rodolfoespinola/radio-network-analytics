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

try:
    import plotly.express as px
    PLOTLY_DISPONIVEL = True
except ImportError:
    PLOTLY_DISPONIVEL = False
    print("  ⚠ plotly não instalado — mapa interativo será ignorado")

DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / "cache"
OUTPUT_DIR = Path("outputs")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

TAXA_ESCUTA_RADIO = 0.80
LIMIAR_LACUNA    = 5_000
LIMIAR_ESTRATEGICO = 30_000
TOP_N_RADIOS = 10
POP_SC_TOTAL = 7_610_361

COR_PRINCIPAL  = "#1a6fa8"
COR_ALERTA     = "#c0392b"
COR_POSITIVO   = "#27ae60"
COR_SECUNDARIA = "#e07b39"
COR_MAPA_SC    = "#eaf2ea"

plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.family"] = "DejaVu Sans"
sns.set_style("whitegrid")

# ── Paleta de tipos — 11 cores de alto contraste, sem repetição ───────────────
# Categorias com < 100 registros totais (Especial, Legislação, Podcast)
# são fundidas em "Outros" via Tipo_Plot para não desperdiçar cor
PALETA_TIPO = {
    "Comissão":          "#1a6fa8",   # azul forte
    "Ordem do Dia":      "#27ae60",   # verde
    "Plenário":          "#8e44ad",   # roxo
    "Institucional":     "#16a085",   # verde-água
    "Evento":            "#e67e22",   # laranja
    "Audiência Pública": "#c0392b",   # vermelho
    "Frentes e Bancadas":"#2980b9",   # azul claro
    "Moção":             "#e91e8c",   # rosa choque
    "Sessão":            "#d35400",   # laranja escuro
    "Projeto de Lei":    "#f1c40f",   # amarelo
    "Outros":            "#bdc3c7",   # cinza
}
# Categorias que serão fundidas em "Outros" nos gráficos de mix
CATS_FUNDIR = {"Especial", "Legislação", "Podcast", "Sem categoria"}

# ── Centroides ────────────────────────────────────────────────────────────────
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
Tubarão,-28.4678,-49.0128
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
# Centroides com população — usado exclusivamente no mapa interativo de intensidade
CENTROIDES_POP_CSV = """municipio,lat,lon,pop
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

df_centroides = pd.read_csv(StringIO(CENTROIDES_SC_CSV))
df_centroides["Cidade_norm"] = df_centroides["municipio"].apply(
    lambda x: unicodedata.normalize("NFD", str(x).lower().strip())
              .encode("ascii", "ignore").decode()
)

# ── Funções ───────────────────────────────────────────────────────────────────

def normalizar(texto):
    if pd.isna(texto): return ""
    texto = str(texto).lower().strip().replace("-", " ").replace("'", " ")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def extrair_data_criacao(nome):
    if pd.isna(nome): return pd.NaT
    nome = str(nome).strip()
    nome = re.sub(r'[_\s]+[cC]$', '', nome).strip()
    todas = re.findall(r'\d{8}', nome)
    if todas:
        seq = todas[-1]
        d, mes, ano = int(seq[0:2]), int(seq[2:4]), int(seq[4:8])
        if 1 <= d <= 31 and 1 <= mes <= 12 and 2020 <= ano <= 2030:
            try: return pd.Timestamp(f'{ano}-{mes:02d}-{d:02d}')
            except: pass
        mes_us, d_us, ano_us = int(seq[0:2]), int(seq[2:4]), int(seq[4:8])
        if 1 <= mes_us <= 12 and 1 <= d_us <= 31 and 2020 <= ano_us <= 2030:
            try: return pd.Timestamp(f'{ano_us}-{mes_us:02d}-{d_us:02d}')
            except: pass
    todas6 = re.findall(r'\d{6}', nome)
    if todas6:
        seq = todas6[-1]
        d, mes, ano = int(seq[0:2]), int(seq[2:4]), 2000 + int(seq[4:6])
        if 1 <= d <= 31 and 1 <= mes <= 12 and 2020 <= ano <= 2030:
            try: return pd.Timestamp(f'{ano}-{mes:02d}-{d:02d}')
            except: pass
    return pd.NaT

def normalizar_nomenclatura(nome):
    if pd.isna(nome): return nome
    return str(nome).replace("_", " ").strip()

def categorizar_tipo(nome):
    if pd.isna(nome): return "Sem categoria"
    nome_norm = normalizar_nomenclatura(nome)
    prefixo = nome_norm.strip().upper().split()[0] if nome_norm.strip() else ""
    mapa = {
        "OD":           "Ordem do Dia",
        "ODT":          "Ordem do Dia",
        "ORDEM":        "Ordem do Dia",
        "PL":           "Projeto de Lei",
        "PEC":          "Projeto de Lei",
        "PLS":          "Projeto de Lei",
        "COM":          "Comissão",
        "CCJ":          "Comissão",
        "COMISSÃO":     "Comissão",
        "COMISSAO":     "Comissão",
        "CPM":          "Comissão",
        "SESSAO":       "Sessão",
        "SESSÃO":       "Sessão",
        "SOLENE":       "Sessão",
        "FP":           "Frentes e Bancadas",
        "FRENTE":       "Frentes e Bancadas",
        "BANCADA":      "Frentes e Bancadas",
        "AP":           "Audiência Pública",
        "AUD":          "Audiência Pública",
        "AUDIENCIA":    "Audiência Pública",
        "AUDIÊNCIA":    "Audiência Pública",
        "EVENTO":       "Evento",
        "SEMINÁRIO":    "Evento",
        "SEMINARIO":    "Evento",
        "PALESTRA":     "Evento",
        "ROMARIA":      "Evento",
        "FESTA":        "Evento",
        "FÓRUM":        "Evento",
        "FORUM":        "Evento",
        "LIVRO":        "Evento",
        "SANCIONADOS":  "Legislação",
        "SANÇÃO":       "Legislação",
        "VETO":         "Legislação",
        "DECRETO":      "Legislação",
        "INFORMATIVO":  "Legislação",   
        "INSTITUCIONAL":"Institucional",
        "CHAMADA":      "Institucional",
        "POD":          "Podcast",
        "RF":           "Podcast",        
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
    v = sorted(valores)
    n = len(v)
    if n == 0 or sum(v) == 0: return 0
    cumsum = sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(v))
    return cumsum / (n * sum(v))

def buscar_com_cache(url, cache_path, timeout=15):
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

# ── Função auxiliar para relatórios ──────────────────────────────────────────
def safe_get(df_resumo, ano, col):
    linha = df_resumo[df_resumo["Ano"] == ano]
    if linha.empty or col not in linha.columns: return 0
    vals = linha[col].values
    return int(vals[0]) if len(vals) > 0 else 0

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
        if str(tmp.iloc[0, 1]).strip().lower() == "data":
            tmp = tmp.iloc[2:].reset_index(drop=True)
        tmp.columns = COLUNAS[:len(tmp.columns)]
        tmp["Veiculacoes"] = 1
        tmp = tmp.dropna(subset=[tmp.columns[0]])
        datas = pd.to_datetime(tmp["Data"], dayfirst=True, errors="coerce", format="mixed")
        pct_inv = datas.isna().mean() * 100
        amostra = tmp["Comercial"].dropna().head(50)
        sep = "underscore" if amostra.str.contains("_", na=False).mean() > 0.5 else "espaço"
        tmp["Arquivo"] = arq.name
        dfs.append(tmp)
        relatorio_val.append({
            "Arquivo": arq.name, "Registros": len(tmp), "Separador": sep,
            "Datas_invalidas_pct": f"{pct_inv:.1f}%",
            "Status": "OK" if pct_inv < 5 else f"⚠ {pct_inv:.0f}% datas inválidas",
        })
    except Exception as e:
        erros.append(arq.name)
        print(f"  ✗ ERRO em {arq.name}: {e}")
        relatorio_val.append({"Arquivo": arq.name, "Registros": 0, "Separador": "—",
                               "Datas_invalidas_pct": "—", "Status": f"ERRO: {e}"})

df_val = pd.DataFrame(relatorio_val)
print(df_val[["Arquivo","Registros","Separador","Status"]].to_string(index=False))
df_val.to_csv(OUTPUT_DIR / "00_relatorio_validacao.csv", index=False)

# ══════════════════════════════════════════════════════════════════════════════
# 2. CONSOLIDAÇÃO E LIMPEZA
# ══════════════════════════════════════════════════════════════════════════════
print("\n[2/8] Consolidando dados...")

df = pd.concat(dfs, ignore_index=True)
df[["Cidade", "UF"]] = df["Cidade_UF"].str.extract(r"^(.+?)\s*/\s*(\w{2})$")
df["UF"]          = df["Cidade_UF"].str.extract(r"/\s*(\w{2})$")[0].str.strip().fillna("SC")
df["Cidade"]      = df["Cidade"].str.strip()
df["Data"]        = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce", format="mixed")
df                = df.dropna(subset=["Data"])
df["Ano"]         = df["Data"].dt.year.astype(int)
df["Mes"]         = df["Data"].dt.month
df["AnoMes"]      = df["Data"].dt.to_period("M")
df["Hora_dt"]     = pd.to_datetime(df["Hora"], format="%H:%M:%S", errors="coerce")
df["Hora_int"]    = df["Hora_dt"].dt.hour
df["Cidade_norm"] = df["Cidade"].apply(normalizar)

# Fallback Peca→Comercial (recupera registros de 2024 com coluna deslocada)
mask_fallback = df["Comercial"].isna() & df["Peca"].notna()
df.loc[mask_fallback, "Comercial"] = df.loc[mask_fallback, "Peca"]
if mask_fallback.sum() > 0:
    print(f"  ✓ Fallback Peca→Comercial: {mask_fallback.sum():,} registros recuperados")

df["Tipo"]         = df["Comercial"].apply(categorizar_tipo)

# Tipo_Plot: funde categorias pequenas em Outros para uso nos gráficos
df["Tipo_Plot"]    = df["Tipo"].apply(lambda t: "Outros" if t in CATS_FUNDIR else t)

df["Data_Criacao"] = df["Comercial"].apply(extrair_data_criacao)
df["Data_Criacao"] = pd.to_datetime(df["Data_Criacao"], errors="coerce")
df["Dias_Ate_Veiculacao"] = (df["Data"] - df["Data_Criacao"]).dt.days
# df["Radio_norm"] = df["Radio"].apply(normalizar)
# df["Radio_norm"]   = df["Radio"].str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)

def normalizar_radio(texto):
    if pd.isna(texto): return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r'\s+', ' ', texto)
    return texto

df["Radio_norm"] = df["Radio"].apply(normalizar_radio)

RADIO_ALIAS = {
    # Atalaia Campo Erê AM→FM 106.1
    "atalaia - am (106.1)":                        "atalaia - fm (106.1)",

    # Blumenau FM 89.1
    "rede clube - fm (89.1)":                      "clube - fm (89.1)",

    # Blumenau FM 106.3
    "mix (indaial) - fm (106.3)":                  "106 - fm (106.3)",

    # Caibi FM 96.7
    "nossa radio - fm (96.7)":                     "caibi - fm (96.7)",

    # Chapecó FM 98.9
    "super conda - fm (98.9)":                     "conda - fm (98.9)",

    # Concórdia FM 101.7
    "alianca - fm (101.7)":                        "massa - fm (101.7)",

    # Criciúma FM 89.1
    "cidade em dia (ararangua) - fm (89.1)":       "cidade em dia - fm (89.1)",

    # Criciúma FM 89.5
    "eldorado mais (sideropolis) - fm (89.5)":     "eldorado - fm (89.5)",

    # Criciúma FM 92.5
    "92 (ararangua) - fm (92.5)":                 "92 - fm (92.5)",

    # Criciúma FM 104.3
    "jovem pan news (nova veneza) - fm (104.3)":   "jovem pan - fm (104.3)",
    "jovem pan (nova veneza) - fm (104.3)":        "jovem pan - fm (104.3)",

    # Dona Emma FM 87.9
    "radio atitude - fm (87.9)":                   "atitude - fm (87.9)",

    # Garuva FM 96.7
    "maxima - fm (96.7)":                          "maxima hits - fm (96.7)",

    # Irineópolis FM 105.9
    # "nossa radio - fm (105.9)":                    "planalto - fm (105.9)",

    # Itajaí FM 102.1
    "clube litoral norte - fm (102.1)":            "rede clube litoral norte - fm (102.1)",
    "rede clube - fm (102.1)":                     "rede clube litoral norte - fm (102.1)",

    # Jaraguá do Sul FM 105.7 — ADICIONAR
    "105 - fm (105.7)":                            "105 (guaramirim) - fm (105.7)",
    
    # Jovem Pan News Difusora Rio do Sul FM 93.9
    "jovem pan news difusora - fm (93.9)":         "jovem pan news difusora - fm (93.9)",

    # Jovem Pan News Tubarão FM 95.9
    "jovem pan news (imarui) - fm (95.9)":         "jovem pan news - fm (95.9)",

    # Orleans FM 106.3
    "luz e vida - comunitaria (106.3)":            "luz e vida - fm (106.3)",

    # Palmitos FM 101.5
    "101 - fm (101.5)":                            "nossa radio palm - fm (101.5)",
    "nossa radio - fm (101.5)":                    "nossa radio palm - fm (101.5)",
    "a nossa radio - fm (101.5)":                  "nossa radio palm - fm (101.5)",

    # Passos Maia FM 100.7
    "100.7 - fm (100.7)":                          "nossa radio passos - fm (100.7)",
    "a nossa radio - fm (100.7)":                  "nossa radio passos - fm (100.7)",

    # Rio do Sul FM 98.5
    "98.5 - fm (98.5)":                            "mirador - fm (98.5)",

    # São Carlos FM 104.1
    "104 - fm (104.1)":                            "nossa radio sao carlos - fm (104.1)",
    "nossa radio - fm (104.1)":                    "nossa radio sao carlos - fm (104.1)",
    "a nossa radio - fm (104.1)":                  "nossa radio sao carlos - fm (104.1)",

    # Sombrio FM 102.9
    "102.9 - fm (102.9)":                          "amorim - fm (102.9)",

    # Stylo Braço do Norte FM 102.1
    "stylo (grao para) - fm (102.1)":              "stylo - fm (102.1)",

    # Timbó FM 92.1
    "cultura - fm (92.1)":                         "cultura 92 - fm (92.1)",

    # Vanguarda Xaxim FM 95.5
    "vang - fm (95.5)":                            "vanguarda - fm (95.5)",

    # Videira FM 102.9
    "radio v - fm (102.9)":                        "v - fm (102.9)",
}

# Aplica normalização — substitui Radio_norm pelos nomes canônicos
n_antes = df["Radio_norm"].nunique()
df["Radio_norm"] = df["Radio_norm"].replace(RADIO_ALIAS)
n_depois = df["Radio_norm"].nunique()
print(f"  ✓ Normalização de rádios: {n_antes} → {n_depois} nomes únicos "
      f"({n_antes - n_depois} duplicatas consolidadas)")

# Atualiza também o campo Radio para exibição (usa o nome do registro mais recente)
mapa_display = (df.sort_values("Data")
                  .drop_duplicates("Radio_norm", keep="last")
                  .set_index("Radio_norm")["Radio"]
                  .to_dict())
df["Radio"] = df["Radio_norm"].map(mapa_display).fillna(df["Radio"])

df = df.dropna(subset=["Cidade_UF"])

anos = sorted(df["Ano"].unique())
anos_validos = sorted([a for a in anos if a >= 2020])
# Último ano com dados completos (12 meses). Usado para excluir anos parciais de métricas de taxa.
ultimo_ano_completo = max(
    (a for a in anos_validos if df[df["Ano"] == a]["Mes"].nunique() == 12),
    default=anos_validos[-1]
)

print(f"  ✓ {len(df):,} registros | {df['Radio'].nunique()} rádios | "
      f"{df['Cidade'].nunique()} cidades | {anos_validos}")
for ano in anos_validos:
    print(f"    {ano}: {(df['Ano']==ano).sum():,} veiculações")

df_ciclo = df[
    df["Dias_Ate_Veiculacao"].notna() &
    (df["Dias_Ate_Veiculacao"] >= 0) &
    (df["Dias_Ate_Veiculacao"] <= 365)
].copy()
pct_ciclo = len(df_ciclo) / len(df) * 100
print(f"  ✓ Ciclo de vida: {len(df_ciclo):,} registros com data extraída ({pct_ciclo:.1f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 3. POPULAÇÃO IBGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3/8] Dados IBGE...")

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
        url = ("https://servicodados.ibge.gov.br/api/v3/agregados/4714"
               "/periodos/2022/variaveis/all?localidades=N6[in N3[42]]")
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        dados = r.json()
        cache_path.write_text(json.dumps([dados[0]]), encoding="utf-8")
        print("  ✓ População IBGE: carregada via API (Censo 2022)")

    registros = []
    for item in dados[0]["resultados"][0]["series"]:
        nome = item["localidade"]["nome"].replace(" - SC", "").strip()
        pop  = item["serie"].get("2022")
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

if df_pop is not None:
    df = df.merge(df_pop[["Cidade_norm", "Populacao"]], on="Cidade_norm", how="left")
    mediana_pop    = df_pop["Populacao"].median()
    sem_match_mask = df["Populacao"].isna()
    n_sem_match    = sem_match_mask.sum()
    df["Populacao"] = df["Populacao"].fillna(mediana_pop)
    if n_sem_match > 0:
        print(f"  ⚠ {n_sem_match} registros sem match IBGE — fallback mediana ({mediana_pop:,.0f} hab.)")
        for c in sorted(df[sem_match_mask]["Cidade_UF"].unique())[:10]:
            print(f"    → {c}")
    else:
        print("  ✓ Todas as cidades com match no IBGE")
else:
    sem_match_mask = pd.Series(False, index=df.index)
    df["Populacao"] = 12_000

df["Audiencia_Unica"] = df["Populacao"] * TAXA_ESCUTA_RADIO

df_centroides["Cidade_norm"] = df_centroides["municipio"].apply(normalizar)
print(f"  ✓ Centroides: {len(df_centroides)} municípios (embutidos)")

extras_centroides = pd.DataFrame([
    {"municipio": k, "Cidade_norm": k, "lat": v["lat"], "lon": v["lon"]}
    for k, v in CIDADES_FRONTEIRA.items()
])
df_centroides = pd.concat([df_centroides, extras_centroides], ignore_index=True)
print(f"  ✓ Centroides: {len(df_centroides)} municípios (SC + fronteira PR)")

cidades_excel     = set(df["Cidade_norm"].dropna().unique())
cidades_mapa      = set(df_centroides["Cidade_norm"].unique())
cidades_faltantes = cidades_excel - cidades_mapa
if cidades_faltantes:
    print(f"  ⚠ {len(cidades_faltantes)} cidades sem centroide:")
    for c in sorted(cidades_faltantes)[:15]:
        print(f"    → {c}")
    (df[df["Cidade_norm"].isin(cidades_faltantes)][["Cidade","Cidade_norm","Radio"]]
     .drop_duplicates().sort_values("Cidade")
     .to_csv(OUTPUT_DIR / "erros_geograficos.csv", index=False, encoding="utf-8-sig"))
else:
    print("  ✓ 100% das cidades com centroide")

# ══════════════════════════════════════════════════════════════════════════════
# ABRANGÊNCIA REAL DE RÁDIOS
# Inserir logo APÓS o bloco [3/8] POPULAÇÃO IBGE, antes do bloco [4/8] TABELAS BASE
# Requer: df com Radio_norm já aplicado + RADIO_ALIAS já processado
#         df_pop com Cidade_norm e Populacao
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3.1/8] Carregando abrangência real das rádios...")
 
from pathlib import Path as _Path
 
ABRANGENCIA_CSV = _Path("data/radios municipios - mar2026.csv")
 
# ── Constrói tabela Radio_norm → [lista de Cidade_norm de abrangência] ────────
mapa_abrangencia = {}  # Radio_norm → set de Cidade_norm
 
if ABRANGENCIA_CSV.exists():
    raw_abr = pd.read_csv(ABRANGENCIA_CSV, encoding="utf-8",
                          sep=None, engine="python", header=None)
 
    for _, row in raw_abr.iterrows():
        radio_raw = str(row.iloc[0]).strip()
        if pd.isna(row.iloc[0]) or radio_raw == "nan":
            continue
        radio_norm = normalizar_radio(radio_raw)
 
        cidades = []
        for val in row.iloc[1:]:
            if pd.notna(val) and str(val).strip() not in ("nan", ""):
                cidade_raw = str(val).split("/")[0].strip()  # remove "/ SC"
                cidades.append(normalizar(cidade_raw))
 
        if cidades:
            mapa_abrangencia[radio_norm] = set(cidades)
 
    print(f"  ✓ {len(mapa_abrangencia)} rádios com abrangência mapeada")
    n_com = sum(1 for rn in df["Radio_norm"].unique() if rn in mapa_abrangencia)
    n_sem = sum(1 for rn in df["Radio_norm"].unique() if rn not in mapa_abrangencia)
    print(f"  ✓ Match no dataset: {n_com} rádios com abrangência | "
          f"{n_sem} sem (fallback = município sede)")
else:
    print(f"  ⚠ Arquivo não encontrado: {ABRANGENCIA_CSV}")
    print(f"     Coloque o CSV em data/ para usar abrangência real")
 
# ── Calcula população de abrangência por rádio ────────────────────────────────
# Para cada Radio_norm: soma pop. de todos os municípios de abrangência
# Para rádios sem mapeamento: usa população do município sede (comportamento anterior)
 
def pop_abrangencia(radio_norm, cidade_sede_norm, df_pop_ref):
    """Retorna população total de abrangência da rádio."""
    if radio_norm in mapa_abrangencia and df_pop_ref is not None:
        cids = mapa_abrangencia[radio_norm]
        pop  = df_pop_ref[df_pop_ref["Cidade_norm"].isin(cids)]["Populacao"].sum()
        return int(pop) if pop > 0 else None
    return None  # None = usar fallback do município sede
 
# Cria coluna Pop_Abrangencia no df principal
if df_pop is not None and mapa_abrangencia:
    df["Pop_Abrangencia"] = df.apply(
        lambda row: pop_abrangencia(row["Radio_norm"], row["Cidade_norm"], df_pop),
        axis=1
    )
    # Fallback: onde não há abrangência mapeada, usa população do município sede
    df["Pop_Abrangencia"] = df["Pop_Abrangencia"].fillna(df["Populacao"])
 
    n_com_abr = df["Pop_Abrangencia"].notna().sum()
    media_abr = df[df["Radio_norm"].isin(mapa_abrangencia)]["Pop_Abrangencia"].mean()
    media_sed = df[~df["Radio_norm"].isin(mapa_abrangencia)]["Populacao"].mean()
    print(f"  ✓ Pop. média com abrangência real: {media_abr:,.0f} hab.")
    print(f"  ✓ Pop. média fallback (sede):      {media_sed:,.0f} hab.")
else:
    df["Pop_Abrangencia"] = df["Populacao"]
 
# Audiência potencial com abrangência real
df["Audiencia_Abrangencia"] = df["Pop_Abrangencia"] * TAXA_ESCUTA_RADIO

# Cobertura por ano com abrangência real (calculada abaixo, após o bloco de cobertura)
'''
if df_pop is not None:
    pop_coberta_ano = []
    for ano in anos_validos:
        # Municípios com veiculação direta
        cids_veiculacao = set(df[df["Ano"]==ano]["Cidade_norm"].dropna().unique())
        # Municípios cobertos por abrangência das rádios ativas no ano
        rads_ano = set(df[df["Ano"]==ano]["Radio_norm"].dropna().unique())
        cids_abrangencia = set()
        for rn in rads_ano:
            if rn in mapa_abrangencia:
                cids_abrangencia.update(mapa_abrangencia[rn])
        # União
        cids_total = cids_veiculacao | cids_abrangencia
        pop = df_pop[df_pop["Cidade_norm"].isin(cids_total)]["Populacao"].sum()
        pop_coberta_ano.append({"Ano": ano, "Pop_Coberta": pop})
    cobertura_ano = cobertura_ano.merge(pd.DataFrame(pop_coberta_ano), on="Ano")
    cobertura_ano["Pct_Pop_SC"] = cobertura_ano["Pop_Coberta"] / POP_SC_TOTAL * 100
'''
if df_pop is not None:
    dados_cobertura_ano = []
    for ano in anos_validos:
        # 1. Rádios ativas no ano
        df_ano = df[df["Ano"] == ano]
        rads_ano = set(df_ano["Radio_norm"].dropna().unique())
        
        # 2. Municípios sede (veiculação direta)
        cids_veiculacao = set(df_ano["Cidade_norm"].dropna().unique())
        
        # 3. Municípios alcançados via abrangência
        cids_abrangencia = set()
        for rn in rads_ano:
            if rn in mapa_abrangencia:
                cids_abrangencia.update(mapa_abrangencia[rn])
        
        # 4. União de TODAS as cidades impactadas
        cids_total = cids_veiculacao | cids_abrangencia
        
        # 5. Cálculos de População e Contagem
        pop = df_pop[df_pop["Cidade_norm"].isin(cids_total)]["Populacao"].sum()
        
        dados_cobertura_ano.append({
            "Ano": ano, 
            "Municipios_Alcancados": len(cids_total), # Agora reflete a abrangência!
            "Pop_Coberta": pop,
            "Pct_Pop_SC": (pop / POP_SC_TOTAL) * 100
        })
    
    cobertura_ano = pd.DataFrame(dados_cobertura_ano)
# ══════════════════════════════════════════════════════════════════════════════
# 4. TABELAS BASE
# ══════════════════════════════════════════════════════════════════════════════

# Mapa global Radio_norm → Cidade (construído uma vez, antes do loop)
# Evita problema de drop_duplicates pegar linhas com Cidade nula
mapa_global_cidade = (
    df.dropna(subset=["Cidade","Radio_norm"])
    .groupby("Radio_norm")["Cidade"]
    .first()
    .to_dict()
)
alcance = (
    df.groupby(["Cidade", "Cidade_norm"])
    .agg(Veiculacoes=("Identificador","count"),
         Populacao=("Populacao","first"),
         Audiencia_Unica=("Audiencia_Unica","first"),
         Audiencia_Abrangencia=("Audiencia_Abrangencia","first"))   # ← adicionar
    .reset_index()
)
alcance["Alcance_Ponderado"]  = alcance["Veiculacoes"] * alcance["Populacao"]
alcance["Indice_Intensidade"] = alcance["Veiculacoes"] / alcance["Populacao"] * 10_000
alcance = alcance.merge(df_centroides[["Cidade_norm","lat","lon"]], on="Cidade_norm", how="left")

serie_mensal = df.groupby("AnoMes").size().reset_index(name="Veiculacoes")
tipo_count   = df["Tipo"].value_counts()

cidades_cobertas = set(df["Cidade_norm"].dropna().unique())
lacunas = pd.DataFrame()
if mapa_abrangencia and df_pop is not None:
    # Municípios cobertos por abrangência direta das veiculações
    radios_ativas = set(df["Radio_norm"].dropna().unique())
    municipios_abrangencia = set()
    for rn in radios_ativas:
        if rn in mapa_abrangencia:
            municipios_abrangencia.update(mapa_abrangencia[rn])
        else:
            # Fallback: município sede da rádio
            sede = df[df["Radio_norm"]==rn]["Cidade_norm"].dropna()
            if len(sede) > 0:
                municipios_abrangencia.add(sede.iloc[0])
 
    # Municípios cobertos apenas por registro direto de veiculação
    municipios_veiculacao = set(df["Cidade_norm"].dropna().unique())
 
    # União: coberto por qualquer meio
    municipios_cobertos_real = municipios_abrangencia | municipios_veiculacao
 
    df_pop["coberto_abrangencia"] = df_pop["Cidade_norm"].isin(municipios_cobertos_real)
    df_pop["coberto_veiculacao"]  = df_pop["Cidade_norm"].isin(municipios_veiculacao)
 
    lacunas_real = (df_pop[~df_pop["coberto_abrangencia"]]
                    .query(f"Populacao > {LIMIAR_LACUNA}")
                    .sort_values("Populacao", ascending=False)
                    .head(15))

    # Lacunas mensais: municípios >30k sem cobertura no mês mais recente do dataset
    # (nem veiculação direta nem abrangência de sinal de rádio que veiculou naquele mês)
    ultimo_mes = df["AnoMes"].max()
    df_mes = df[df["AnoMes"] == ultimo_mes]
    radios_mes = set(df_mes["Radio_norm"].dropna().unique())
    municipios_abr_mes = set()
    for rn in radios_mes:
        if rn in mapa_abrangencia:
            municipios_abr_mes.update(mapa_abrangencia[rn])
        else:
            sede = df_mes[df_mes["Radio_norm"] == rn]["Cidade_norm"].dropna()
            if len(sede) > 0:
                municipios_abr_mes.add(sede.iloc[0])
    municipios_veiculacao_mes = set(df_mes["Cidade_norm"].dropna().unique())
    municipios_cobertos_mes = municipios_abr_mes | municipios_veiculacao_mes
    df_pop["coberto_mes"] = df_pop["Cidade_norm"].isin(municipios_cobertos_mes)
    lacunas_mensais = (df_pop[~df_pop["coberto_mes"]]
                       .query(f"Populacao > {LIMIAR_ESTRATEGICO}")
                       .sort_values("Populacao", ascending=False)
                       .head(15))
    print(f"     Lacunas mensais ({ultimo_mes}, >{LIMIAR_ESTRATEGICO//1000}k hab.): {len(lacunas_mensais)} cidades")

    n_cobertos_abr = df_pop["coberto_abrangencia"].sum()
    pop_coberta_abr = df_pop[df_pop["coberto_abrangencia"]]["Populacao"].sum()
 
    print(f"\n  ── Cobertura com abrangência real:")
    print(f"     Municípios cobertos: {n_cobertos_abr} de {len(df_pop)} "
          f"({n_cobertos_abr/len(df_pop)*100:.1f}%)")
    print(f"     Pop. coberta: {pop_coberta_abr:,.0f} hab. "
          f"({pop_coberta_abr/POP_SC_TOTAL*100:.1f}% de SC)")
    print(f"     Lacunas reais (>{LIMIAR_LACUNA//1000}k hab.): {len(lacunas_real)} cidades")
else:
    lacunas_real = lacunas  # fallback para o cálculo anterior
    lacunas_mensais = pd.DataFrame()
    ultimo_mes = df["AnoMes"].max()
    municipios_cobertos_real = set(df["Cidade_norm"].dropna().unique())
    print("  ⚠ Abrangência não disponível — lacunas calculadas pelo método anterior")
 

gini_val = gini(alcance["Veiculacoes"].tolist())

churn_data = []
for i, ano in enumerate(anos_validos):
    radios_ano = set(df[df["Ano"] == ano]["Radio_norm"])
    if i == 0:
        novas  = len(radios_ano)
        saidas = 0
    else:
        radios_ano_anterior = set(df[df["Ano"] == anos_validos[i-1]]["Radio_norm"])
        novas  = len(radios_ano - radios_ano_anterior)
        saidas = len(radios_ano_anterior - radios_ano)
    churn_data.append({"Ano": ano, "Novas": novas, "Saidas": -saidas,
                       "Total_Ativas": len(radios_ano)})
df_churn = pd.DataFrame(churn_data)
'''
historico_acumulado = set()
churn_data = []
for i, ano in enumerate(anos_validos):
    radios_ano = set(df[df["Ano"] == ano]["Radio_norm"])
    novas  = len(radios_ano - historico_acumulado) if i > 0 else len(radios_ano)
    saidas = len(historico_acumulado - radios_ano) if i > 0 else 0
    historico_acumulado.update(radios_ano)
    churn_data.append({"Ano": ano, "Novas": novas, "Saidas": -saidas,
                       "Total_Ativas": len(radios_ano)})
df_churn = pd.DataFrame(churn_data)
'''

'''
radio_ano = df.groupby(["Radio","Ano"]).size().reset_index(name="Veiculacoes")
fidelidade = (
    radio_ano.groupby("Radio")
    .agg(Anos_Ativo=("Ano","nunique"), Total_Veiculacoes=("Veiculacoes","sum"),
         Primeiro_Ano=("Ano","min"), Ultimo_Ano=("Ano","max"))
    .reset_index()
)
'''
radio_ano = df.groupby(["Radio_norm","Ano"]).size().reset_index(name="Veiculacoes")
fidelidade = (
    radio_ano.groupby("Radio_norm")
    .agg(Anos_Ativo=("Ano","nunique"), Total_Veiculacoes=("Veiculacoes","sum"),
         Primeiro_Ano=("Ano","min"), Ultimo_Ano=("Ano","max"))
    .reset_index()
)
# Taxa_Fidelidade calculada apenas sobre anos completos para evitar distorção do ano parcial.
# Rádios ativas só no ano parcial ficam com Taxa_Fidelidade = NaN (dados insuficientes).
radio_ano_completo = radio_ano[radio_ano["Ano"] <= ultimo_ano_completo]
fid_completo = (
    radio_ano_completo.groupby("Radio_norm")
    .agg(Anos_Ativo_Completo=("Ano","nunique"),
         Primeiro_Ano_Completo=("Ano","min"),
         Ultimo_Ano_Completo=("Ano","max"))
    .reset_index()
)
fid_completo["Anos_Possiveis"] = (
    fid_completo["Ultimo_Ano_Completo"] - fid_completo["Primeiro_Ano_Completo"] + 1
)
fid_completo["Taxa_Fidelidade"] = (
    fid_completo["Anos_Ativo_Completo"] / fid_completo["Anos_Possiveis"] * 100
).round(1)
fidelidade = fidelidade.merge(
    fid_completo[["Radio_norm","Taxa_Fidelidade"]], on="Radio_norm", how="left"
)
fidelidade["Anos_Possiveis"] = fidelidade["Ultimo_Ano"] - fidelidade["Primeiro_Ano"] + 1
# 1. Nome canônico de exibição — precisa vir ANTES de Cidade
fidelidade["Radio"]  = fidelidade["Radio_norm"].map(mapa_display).fillna(fidelidade["Radio_norm"])

# 2. Cidade — agora Radio já existe
fidelidade["Cidade"] = fidelidade["Radio_norm"].map(mapa_global_cidade).fillna("")

impacto_radio = (
    df.groupby(["Radio_norm", "Cidade"])
    .agg(
        Veiculacoes_Cidade  = ("Identificador", "count"),
        Pop_Sede            = ("Populacao",       "first"),
        Pop_Abrangencia     = ("Pop_Abrangencia", "first"),
    )
    .reset_index()
    .groupby("Radio_norm")
    .agg(
        Veiculacoes         = ("Veiculacoes_Cidade",  "sum"),
        Impacto_Sede        = ("Pop_Sede",            "sum"),
        Impacto_Abrangencia = ("Pop_Abrangencia",     "max"),
        Cidades_Veiculadas  = ("Cidade",              "nunique"),
    )
    .reset_index()
    .sort_values("Impacto_Abrangencia", ascending=False)
)
# Traz nome de exibição
impacto_radio["Radio"] = impacto_radio["Radio_norm"].map(mapa_display).fillna(impacto_radio["Radio_norm"])
# Traz cidades de abrangência (contagem)
impacto_radio["Municipios_Abrangencia"] = impacto_radio["Radio_norm"].map(
    lambda rn: len(mapa_abrangencia[rn]) if rn in mapa_abrangencia else 1
)

ciclo_tipo = (
    df_ciclo.groupby("Tipo")["Dias_Ate_Veiculacao"]
    .agg(Media_dias="mean", Mediana_dias="median", Max_dias="max", Veiculacoes="count")
    .round(1).sort_values("Mediana_dias", ascending=False).reset_index()
)
ciclo_comercial = (
    df_ciclo.groupby("Comercial")["Dias_Ate_Veiculacao"]
    .agg(Dias_min_ate_veiculacao="min", Dias_max_ate_veiculacao="max", Total_veiculacoes="count",
         Vida_util_dias=lambda x: x.max() - x.min())
    .sort_values("Vida_util_dias", ascending=False).reset_index()
)
zumbis = (
    df_ciclo[df_ciclo["Dias_Ate_Veiculacao"] > 30]
    .groupby("Comercial")
    .agg(Veiculacoes_tardias=("Comercial","count"), Max_dias=("Dias_Ate_Veiculacao","max"),
         Tipo=("Tipo","first"))
    .sort_values("Max_dias", ascending=False).reset_index()
)
'''
# ============================================================
# 🔽 VERSÃO FINAL REVISADA (FIX: NameError mapa_sede)
# ============================================================
print("\n[DEBUG] Aplicando travas de segurança e normalização de chaves...")

# 1. Definição da Coluna de Conteúdo
if "Titulo" in df.columns:
    coluna_conteudo = "Titulo"
elif "Comercial" in df.columns:
    coluna_conteudo = "Comercial"
else:
    df["Conteudo_Generico"] = "Conteúdo Desconhecido"
    coluna_conteudo = "Conteudo_Generico"

print(f"[DEBUG] Usando a coluna: {coluna_conteudo}")

# 2. Criação do Mapa de Sedes (MANTENHA ESTA LINHA AQUI)
# Ele cria um dicionário onde a chave é a rádio e o valor é a cidade sede
mapa_sede = df.groupby("Radio_norm")["Cidade_norm"].first().to_dict()

# 3. Limpeza e Normalização Global
df = df.dropna(subset=[coluna_conteudo])
df_pop = df_pop.drop_duplicates(subset=["Cidade_norm"])
df_pop["Cidade_norm"] = df_pop["Cidade_norm"].astype(str).str.strip().str.lower()
if 'Cidade_norm' in df.columns:
    df["Cidade_norm"] = df["Cidade_norm"].astype(str).str.strip().str.lower()

# 4. Normalização das Referências de Antenas
if 'mapa_muni' in locals():
    mapa_muni = {str(k).strip().lower(): {str(m).strip().lower() for m in v if m} 
                 for k, v in mapa_muni.items()}

if 'df_abr' in locals():
    col_radio_abr = "Radio_norm" if "Radio_norm" in df_abr.columns else "Radio"
    df_abr[col_radio_abr] = df_abr[col_radio_abr].astype(str).str.strip().str.lower()
    
    def norm_lista(x):
        if isinstance(x, list): return [str(m).strip().lower() for m in x if m]
        return [str(x).strip().lower()] if pd.notna(x) else []
    df_abr["Municipios_Abrangencia"] = df_abr["Municipios_Abrangencia"].apply(norm_lista)

# 5. Processamento Principal
total_municipios_sc = df_pop["Cidade_norm"].nunique()
dados_alcance_final = []

for nome_conteudo, grupo in df.groupby(coluna_conteudo):
    radios = grupo["Radio_norm"].dropna().unique()
    municipios_total = set()

    for r in radios:
        encontrou = False
        # A. Busca no mapa_muni
        if 'mapa_muni' in locals() and r in mapa_muni:
            municipios_total.update(mapa_muni[r])
            encontrou = True
        
        # B. Busca no df_abr
        elif 'df_abr' in locals():
            muni_abr = df_abr[df_abr[col_radio_abr] == r]["Municipios_Abrangencia"]
            if not muni_abr.empty:
                for lista in muni_abr:
                    municipios_total.update(lista)
                encontrou = True
        
        # C. Fallback Sede (AGORA O mapa_sede ESTÁ DEFINIDO ACIMA)
        if not encontrou:
            sede = mapa_sede.get(r)
            if sede:
                municipios_total.add(sede)

    # Inclusão de cidades da veiculação direta e normalização final do set
    municipios_total.update(grupo["Cidade_norm"].dropna().unique())
    municipios_total = {str(m).strip().lower() for m in municipios_total if m}

    # Cálculo final de população e cobertura
    pop_total = df_pop[df_pop["Cidade_norm"].isin(municipios_total)]["Populacao"].sum()
    pct_estado = (len(municipios_total) / total_municipios_sc) * 100

    if pop_total > 0:
        dados_alcance_final.append({
            "Conteudo": nome_conteudo,
            "Populacao": int(pop_total),
            "Cidades": len(municipios_total),
            "Cobertura_%": round(pct_estado, 1),
            "Emissoras": len(radios),
            "Eficiencia_Pop": int(pop_total / len(radios)) if len(radios) > 0 else 0
        })

# --- GERAÇÃO DO RANKING ---
if dados_alcance_final:
    df_ranking_final = pd.DataFrame(dados_alcance_final).sort_values("Populacao", ascending=False).reset_index(drop=True)
    caminho_csv = OUTPUT_DIR / "ranking_impacto_alesc_auditado.csv"
    df_ranking_final.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

    print("\n" + "="*75)
    print(f"🏆 RANKING DE IMPACTO REAL E COBERTURA TERRITORIAL")
    print("="*75)
    print(df_ranking_final.head(10)[["Conteudo", "Populacao", "Cidades", "Cobertura_%", "Eficiencia_Pop"]])
    print("="*75)
    print(f"✓ Relatório pronto para apresentação em: {caminho_csv}")
'''
# ══════════════════════════════════════════════════════════════════════════════
# RANKING DE IMPACTO REAL POR CONTEÚDO
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3.2/8] Gerando ranking de impacto por conteúdo...")

if df_pop is not None and "Comercial" in df.columns:
    # Usa cópia local para não cortar df global
    df_rank = df.dropna(subset=["Comercial"]).copy()
    df_pop_rank = df_pop.drop_duplicates(subset=["Cidade_norm"]).copy()

    mapa_sede = df_rank.groupby("Radio_norm")["Cidade_norm"].first().to_dict()
    total_municipios_sc = df_pop_rank["Cidade_norm"].nunique()
    dados_alcance_final = []

    for nome_conteudo, grupo in df_rank.groupby("Comercial"):
        radios = grupo["Radio_norm"].dropna().unique()
        municipios_total = set()

        for r in radios:
            # Usa mapa_abrangencia (construído no bloco 3.1)
            if r in mapa_abrangencia:
                municipios_total.update(mapa_abrangencia[r])
            else:
                sede = mapa_sede.get(r)
                if sede:
                    municipios_total.add(sede)

        # Garante que municípios de veiculação direta também entram
        municipios_total.update(
            {m for m in grupo["Cidade_norm"].dropna().unique() if m}
        )

        pop_total = df_pop_rank[
            df_pop_rank["Cidade_norm"].isin(municipios_total)
        ]["Populacao"].sum()

        pct_estado = len(municipios_total) / total_municipios_sc * 100

        if pop_total > 0:
            dados_alcance_final.append({
                "Conteudo":      nome_conteudo,
                "Populacao":     int(pop_total),
                "Cidades":       len(municipios_total),
                "Cobertura_%":   round(pct_estado, 1),
                "Emissoras":     len(radios),
                "Eficiencia_Pop": int(pop_total / len(radios)) if radios.size > 0 else 0,
            })

    if dados_alcance_final:
        df_ranking_final = (pd.DataFrame(dados_alcance_final)
                            .sort_values("Populacao", ascending=False)
                            .reset_index(drop=True))
        caminho_csv = OUTPUT_DIR / "ranking_impacto_alesc_auditado.csv"
        df_ranking_final.to_csv(caminho_csv, index=False, encoding="utf-8-sig")
        print(f"\n{'='*75}")
        print("🏆 RANKING DE IMPACTO REAL E COBERTURA TERRITORIAL")
        print(f"{'='*75}")
        print(df_ranking_final.head(10)[
            ["Conteudo","Populacao","Cidades","Cobertura_%","Eficiencia_Pop"]
        ].to_string(index=False))
        print(f"{'='*75}")
        print(f"  ✓ {caminho_csv.name} — {len(df_ranking_final):,} conteúdos ranqueados")
    else:
        print("  ⚠ Nenhum conteúdo com população calculada")
else:
    print("  ⚠ Ranking ignorado (df_pop ou coluna Comercial ausentes)")



# ══════════════════════════════════════════════════════════════════════════════
# 5. VISUALIZAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
print("\n[4/8] Gerando gráficos...")

mapa_df = alcance.dropna(subset=["lat","lon"]).copy()

# ── 01 Mapa de cobertura ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
for ax, col, titulo, cmap_n, label in [
    (axes[0],"Veiculacoes","Veiculações por Município","Blues","Veiculações"),
    (axes[1],"Audiencia_Unica","Audiência Potencial Estimada*","Oranges","Pessoas"),
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
            ax.annotate(row["Cidade"], (row["lon"], row["lat"]), fontsize=6.5,
                        ha="center", xytext=(0,7), textcoords="offset points",
                        color="#222", zorder=3)
    ax.set_title(titulo, fontweight="bold", fontsize=11)
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
fig.suptitle("Mapa de Cobertura da Rádio Alesc — Santa Catarina\n"
             "(tamanho proporcional à população)", fontweight="bold")
nota_rodape(axes[1], f"*Audiência potencial = pop. × {TAXA_ESCUTA_RADIO} (ACAERT 2024)")
fig.tight_layout()
salvar(fig, "01_mapa_cobertura_sc.png")

# ── 02 Evolução de cobertura territorial por ano ──────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 7))
x = [str(a) for a in cobertura_ano["Ano"]]
bars = ax1.bar(x, cobertura_ano["Municipios_Alcancados"],
               color=COR_PRINCIPAL, alpha=0.3, label="Municípios", width=0.6)
ax1.set_ylabel("Municípios alcançados", color=COR_PRINCIPAL, fontweight="bold")
ax1.set_title("Evolução da Cobertura Territorial e Populacional\n(Rádio Alesc 2023–2026)",
              fontweight="bold", fontsize=14, pad=25)
ax1.set_ylim(0, cobertura_ano["Municipios_Alcancados"].max() * 1.25)
for bar in bars:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h, f"{int(h)}",
             ha="center", va="bottom", fontsize=11, fontweight="bold", color=COR_PRINCIPAL)
if "Pct_Pop_SC" in cobertura_ano.columns:
    ax2 = ax1.twinx()
    ax2.plot(x, cobertura_ano["Pct_Pop_SC"], marker="o", color=COR_ALERTA,
             linewidth=3, markersize=10, label="% pop. SC", zorder=5)
    ax2.set_ylabel("% da população de SC", color=COR_ALERTA, fontweight="bold")
    ax2.set_ylim(0, 100)
    for i, pct in enumerate(cobertura_ano["Pct_Pop_SC"]):
        ax2.annotate(f"{pct:.1f}%", (x[i], pct), xytext=(0,12),
                     textcoords="offset points", ha="center", fontsize=10,
                     color=COR_ALERTA, fontweight="bold",
                     bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))
    ax2.grid(False)
ax1.grid(True, axis='y', linestyle='--', alpha=0.4)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True)
fig.tight_layout()
salvar(fig, "02_cobertura_territorial_por_ano.png")

# ── 03 Série histórica mensal ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(15, 6))
x_mes = serie_mensal["AnoMes"].astype(str)
y_mes = serie_mensal["Veiculacoes"]
serie_mensal["Tendencia"] = y_mes.rolling(window=3, center=True).mean()
ax.plot(x_mes, y_mes, marker="o", color=COR_PRINCIPAL, alpha=0.3, label="Mensal")
ax.plot(x_mes, serie_mensal["Tendencia"], color=COR_PRINCIPAL, linewidth=3, label="Tendência")
ax.fill_between(range(len(x_mes)), y_mes, alpha=0.05, color=COR_PRINCIPAL)
for idx, cor, lbl in [(y_mes.idxmax(), COR_POSITIVO, "PICO"), (y_mes.idxmin(), COR_ALERTA, "VALE")]:
    ax.annotate(f"{lbl}: {y_mes.loc[idx]}", xy=(idx, y_mes.loc[idx]),
                xytext=(0,20), textcoords="offset points", ha="center",
                fontsize=9, color="white", fontweight="bold",
                bbox=dict(boxstyle='round,pad=0.3', fc=cor, ec='none'))
ax.set_title("Evolução Mensal de Veiculações (Com Linha de Tendência)", fontweight="bold", fontsize=14)
n_step = 2 if len(x_mes) > 12 else 1
plt.xticks(range(0, len(x_mes), n_step), x_mes[::n_step], rotation=45, ha="right")
ax.set_ylim(0, y_mes.max() * 1.25)
ax.legend()
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

# ── 05 Comparativo YoY ────────────────────────────────────────────────────────
yoy = df.groupby(["Ano","Mes"]).size().reset_index(name="Veiculacoes")
fig, ax = plt.subplots(figsize=(12, 5))
cores_anos = [COR_PRINCIPAL, COR_SECUNDARIA, COR_POSITIVO, COR_ALERTA]
for i, ano in enumerate(anos_validos):
    d = yoy[yoy["Ano"]==ano].sort_values("Mes")
    ax.plot(d["Mes"], d["Veiculacoes"], marker="o", label=str(ano),
            color=cores_anos[i % len(cores_anos)], linewidth=2)
ax.set_xticks(range(1,13))
ax.set_xticklabels(["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"])
ax.set_ylabel("Veiculações")
ax.set_title("Comparativo Anual por Mês (Year-over-Year) — 2023–2026", fontweight="bold")
ax.legend(title="Ano")
nota_rodape(ax, f"2026 = ano parcial (jan–{df[df['Ano']==anos_validos[-1]]['Mes'].max():02d})")
fig.tight_layout()
salvar(fig, "05_comparativo_yoy.png")

# ── 06 Mix de conteúdo por ano — PALETA CORRIGIDA ────────────────────────────
# Usa Tipo_Plot (com categorias pequenas fundidas) e PALETA_TIPO manual
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
ax.set_ylim(0, 115)
ax.set_title("Evolução do Mix de Conteúdo por Ano — Rádio Alesc (2023–2026)",
             fontsize=13, fontweight="bold", pad=12)
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
ax.spines[["top","right"]].set_visible(False)
totais = df.groupby("Ano").size()
for i, ano in enumerate(anos_validos):
        ax.text(i, 102, f"n={totais.get(ano,0):,}",
            ha="center", fontsize=8, color="#666",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7, edgecolor="none"))
 

handles = [mpatches.Patch(color=PALETA_TIPO.get(c,"#bdc3c7"), label=c)
           for c in ordem_cats if c in tipo_ano.columns]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=6, fontsize=8.5, framealpha=0.9, edgecolor="#ddd", fancybox=True)

ax.text(0.01, 0.99,
        "* Especial, Legislação e Podcast consolidados em 'Outros'  |  2026 = jan–fev",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=7.5, color="#666", style="italic",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.75, edgecolor="none"))
 
plt.tight_layout(rect=[0, 0.1, 1, 1])
salvar(fig, "06_mix_conteudo_por_ano.png")

# ── 07 Churn de rádios ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
x_labels = [str(a) for a in df_churn["Ano"]]
ax.bar(x_labels, df_churn["Novas"],  color=COR_POSITIVO, alpha=0.6, label="Entraram na rede")
ax.bar(x_labels, df_churn["Saidas"], color=COR_ALERTA,   alpha=0.6, label="Saíram da rede")
ax.plot(x_labels, df_churn["Total_Ativas"], color="#333", marker="o",
        linewidth=2.5, markersize=8, label="Total de Rádios Ativas")
for i, row in df_churn.iterrows():
    ax.text(i, row["Novas"] + 1, f"+{int(row['Novas'])}", ha='center',
            color=COR_POSITIVO, fontweight='bold', fontsize=10)
    if row["Saidas"] < 0:
        ax.text(i, row["Saidas"] - 4, f"{int(row['Saidas'])}", ha='center',
                color=COR_ALERTA, fontweight='bold', fontsize=10)
ax.axhline(0, color="black", linewidth=1)
ax.set_title("Movimentação da Rede de Rádios Parceiras\n(Entradas vs. Saídas em relação ao ano anterior)",
             fontweight="bold", fontsize=14, pad=20)
ax.set_ylabel("Quantidade de Emissoras")
ax.set_ylim(df_churn["Saidas"].min() - 15, df_churn["Total_Ativas"].max() + 20)
ax.legend(loc="upper left", frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.3)
nota_rodape(ax, f"Comparação ano a ano  ·  {anos_validos[-1]} = ano parcial (jan–{df[df['Ano']==anos_validos[-1]]['Mes'].max():02d})")
fig.tight_layout()
salvar(fig, "07_churn_radios.png")

# ── 08 Evolução individual das rádios ────────────────────────────────────────
'''
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
'''
radios_multi = radio_ano.groupby("Radio_norm")["Ano"].nunique()
top15 = (radio_ano[radio_ano["Radio_norm"].isin(radios_multi[radios_multi>=2].index)]
         .groupby("Radio_norm")["Veiculacoes"].sum().nlargest(15).index)
df_top = radio_ano[radio_ano["Radio_norm"].isin(top15)]

fig, ax = plt.subplots(figsize=(14, 7))
cores_r = plt.cm.tab20(range(len(top15)))
for i, radio_norm in enumerate(top15):
    d = df_top[df_top["Radio_norm"]==radio_norm].sort_values("Ano")
    label = mapa_display.get(radio_norm, radio_norm)  # nome legível para exibição
    ax.plot(d["Ano"], d["Veiculacoes"], marker="o", linewidth=2,
            markersize=5, color=cores_r[i], label=label)
    ultimo = d.iloc[-1]
    ax.annotate(label.split(" -")[0][:22], (ultimo["Ano"], ultimo["Veiculacoes"]),
                fontsize=6, xytext=(4,0), textcoords="offset points", color=cores_r[i])

ax.set_title("Evolução de Veiculações por Rádio — Top 15 (2023–2026)", fontweight="bold")
ax.set_ylabel("Veiculações por ano"); ax.set_xticks(anos_validos)
ax.legend(fontsize=6.5, ncol=2, loc="upper left", framealpha=0.7)
nota_rodape(ax, "Linhas que chegam a zero = rádio saiu da rede")
fig.tight_layout()
salvar(fig, "08_evolucao_por_radio.png")

# ── 09 Fidelidade das rádios ─────────────────────────────────────────────────
top_fid = fidelidade.sort_values("Total_Veiculacoes", ascending=False).head(20)
cores_fid = [COR_POSITIVO if t==100 else COR_PRINCIPAL if t>=75 else COR_ALERTA
             for t in top_fid["Taxa_Fidelidade"]]
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_fid["Radio"][::-1], top_fid["Taxa_Fidelidade"][::-1], color=cores_fid[::-1])
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

# ── 09b Rádios que precisam de atenção ───────────────────────────────────────
# Critério: Taxa_Fidelidade < 75% E pelo menos 2 anos possíveis de atividade
# (exclui rádios novas que só existem há 1 ano — não é inatividade, é novidade)
# Ordenado por Total_Veiculacoes DESC: parceiras que já foram relevantes primeiro
atencao = (fidelidade[
    (fidelidade["Taxa_Fidelidade"] < 75) &
    (fidelidade["Anos_Possiveis"] >= 2)
]
.sort_values("Total_Veiculacoes", ascending=False)
.head(20))

if not atencao.empty:
    cores_at = [COR_ALERTA if t < 50 else COR_SECUNDARIA
                for t in atencao["Taxa_Fidelidade"]]

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(atencao["Radio"][::-1], atencao["Taxa_Fidelidade"][::-1],
                   color=cores_at[::-1])
    ax.axvline(75, color="#888", linestyle="--", linewidth=1,
               label="Limiar de atenção (75%)")

    # Label: anos ativos / anos possíveis + total de veiculações
    for bar, (_, row) in zip(bars, atencao[::-1].iterrows()):
        label = f"{int(row['Anos_Ativo'])}/{int(row['Anos_Possiveis'])} anos  |  {int(row['Total_Veiculacoes'])} veic."
        ax.text(bar.get_width() + 1,
                bar.get_y() + bar.get_height() / 2,
                label, va="center", fontsize=7, color="#333")

    ax.set_xlabel("Taxa de fidelidade (%)")
    ax.set_xlim(0, 105)
    ax.set_title("Rádios Parceiras que Precisam de Atenção\n"
                 "(fidelidade <75% com histórico de ≥2 anos)",
                 fontweight="bold")

    patches_at = [
        mpatches.Patch(color=COR_ALERTA,    label="<50% — risco alto de perda"),
        mpatches.Patch(color=COR_SECUNDARIA, label="50–74% — atenção necessária"),
    ]
    ax.legend(handles=patches_at, fontsize=8, loc="lower right")
    nota_rodape(ax, "Ordenado por volume histórico — parceiras que já foram relevantes aparecem primeiro")
    fig.tight_layout()
    salvar(fig, "09b_radios_atencao.png")
else:
    print("  ✓ Nenhuma rádio com fidelidade <75% e ≥2 anos de histórico")

'''# ── 10 Ranking de rádios por impacto ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 8))
'''
top_imp = impacto_radio.head(15)
ax.barh(top_imp["Radio"][::-1], top_imp["Impacto_Abrangencia"][::-1]/1e6, color=COR_SECUNDARIA)
'''
top_imp = impacto_radio.head(15).copy()
top_imp["Radio_Cidade"] = top_imp.apply(
    lambda r: f"{r['Radio'].split(' -')[0][:25]}\n{r['Cidade']}" if r['Cidade'] else r['Radio'].split(' -')[0][:30],
    axis=1
)
ax.set_xlabel("Impacto (população de abrangência — M hab.)")
ax.set_title("Top 15 Rádios por Impacto Real* — Histórico Total", fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.1f}M"))
nota_rodape(ax, "*Impacto = pop. total dos municípios no sinal da rádio (abrangência real)")
fig.tight_layout()
salvar(fig, "10_ranking_radios_por_impacto.png")
'''
# ── 10 Ranking de rádios por impacto ─────────────────────────────────────────
# ── 10 Ranking de rádios por impacto ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 8))
top_imp = impacto_radio.head(15).copy()
top_imp["Radio_Cidade"] = top_imp["Radio_norm"].apply(
    lambda rn: (
        f"{mapa_display.get(rn, rn).split(' -')[0][:25]}\n"
        f"{mapa_global_cidade.get(rn, '')}"
    )
)
ax.barh(top_imp["Radio_Cidade"][::-1], top_imp["Impacto_Abrangencia"][::-1]/1e6, color=COR_SECUNDARIA)
ax.set_xlabel("Impacto (população de abrangência — M hab.)")
ax.set_title("Top 15 Rádios por Impacto Real* — Histórico Total", fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.1f}M"))
nota_rodape(ax, "*Impacto = pop. total dos municípios no sinal da rádio (abrangência real)")
fig.tight_layout()
salvar(fig, "10_ranking_radios_por_impacto.png")

# ── 11 Lacunas mensais + lacunas históricas ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# axes[0] — Lacunas do mês mais recente (sem cobertura direta nem por abrangência)
ax = axes[0]
if not lacunas_mensais.empty:
    ax.barh(lacunas_mensais["Municipio_IBGE"][::-1],
            lacunas_mensais["Populacao"][::-1] / 1000,
            color=COR_ALERTA)
    ax.set_xlabel("População (mil habitantes)")
    ax.set_title(
        f"Lacunas do Mês — {ultimo_mes}\n"
        f"Cidades >{LIMIAR_ESTRATEGICO//1000}k hab. sem veiculação direta ou por abrangência",
        fontweight="bold"
    )
    nota_rodape(ax, "Sem veiculação direta = conteúdo Alesc não produzido/enviado para a cidade  |  "
                    "Sem abrangência = fora do sinal de qualquer rádio parceira ativa no mês")
else:
    ax.text(0.5, 0.5, "Todas as cidades >30k foram alcançadas\nneste mês", ha="center", va="center",
            transform=ax.transAxes, fontsize=12, color="#4caf50")
    ax.set_title(f"Lacunas do Mês — {ultimo_mes}\nCidades >{LIMIAR_ESTRATEGICO//1000}k hab.",
                 fontweight="bold")

# axes[1] — Lacunas históricas acumuladas (todo o período do dataset)
ax = axes[1]
if not lacunas_real.empty:
    ax.barh(lacunas_real["Municipio_IBGE"][::-1],
            lacunas_real["Populacao"][::-1] / 1000,
            color="#e57373")
    ax.set_xlabel("População (mil habitantes)")
    ax.set_title(
        f"Lacunas Históricas — Acumulado\n"
        f"Cidades >{LIMIAR_LACUNA//1000}k hab. nunca alcançadas (direto ou por abrangência)",
        fontweight="bold"
    )
    nota_rodape(ax, "Acumulado desde o início do dataset  |  Cada cidade = oportunidade de expansão de parceria")
else:
    ax.text(0.5, 0.5, "Sem lacunas acima do limiar", ha="center", va="center",
            transform=ax.transAxes, fontsize=12)
    ax.set_title("Lacunas Históricas — Acumulado", fontweight="bold")

fig.tight_layout()
salvar(fig, "11_lacunas_mensal_e_historico.png")
'''
# ── 12 Municípios por mês ─────────────────────────────────────────────────────
mun_mes = df.groupby("AnoMes")["Cidade"].nunique().reset_index(name="Municipios")
fig, ax = plt.subplots(figsize=(14, 5))
x = mun_mes["AnoMes"].astype(str)
ax.plot(x, mun_mes["Municipios"], marker="o", color=COR_SECUNDARIA, linewidth=2, markersize=4)
ax.fill_between(range(len(x)), mun_mes["Municipios"], alpha=0.1, color=COR_SECUNDARIA)
ax.axhline(mun_mes["Municipios"].mean(), color="#888", linestyle="--", linewidth=1)
ax.set_title("Municípios Alcançados por Mês — 2023–2026", fontweight="bold")
ax.set_ylabel("Municípios únicos")
plt.xticks(range(len(x)), x, rotation=60, ha="right", fontsize=7)
fig.tight_layout()
salvar(fig, "12_municipios_por_mes.png")
'''
# ── 12 Municípios por mês — com abrangência real ─────────────────────────────
mun_mes_direto = df.groupby("AnoMes")["Cidade_norm"].nunique().reset_index(name="Direto")

if mapa_abrangencia:
    linhas_abr_mes = []
    for anomes, grp in df.groupby("AnoMes"):
        # Municípios com veiculação direta
        cids_direto = set(grp["Cidade_norm"].dropna().unique())
        # Municípios por abrangência das rádios ativas neste mês
        cids_abrangencia = set()
        for rn in grp["Radio_norm"].dropna().unique():
            if rn in mapa_abrangencia:
                cids_abrangencia.update(mapa_abrangencia[rn])
            else:
                sede = grp[grp["Radio_norm"]==rn]["Cidade_norm"].dropna()
                if len(sede) > 0:
                    cids_abrangencia.add(sede.iloc[0])
        linhas_abr_mes.append({
            "AnoMes":     anomes,
            "Direto":     len(cids_direto),
            "Abrangencia":len(cids_direto | cids_abrangencia),
        })
    mun_mes = pd.DataFrame(linhas_abr_mes).sort_values("AnoMes")
else:
    mun_mes = mun_mes_direto.copy()
    mun_mes["Abrangencia"] = mun_mes["Direto"]

fig, ax = plt.subplots(figsize=(14, 5))
x = mun_mes["AnoMes"].astype(str)

# Linha de abrangência real (total)
ax.fill_between(range(len(x)), mun_mes["Abrangencia"],
                alpha=0.12, color=COR_PRINCIPAL)
ax.plot(x, mun_mes["Abrangencia"], marker="o", color=COR_PRINCIPAL,
        linewidth=2, markersize=4, label="Com abrangência real")

# Linha de veiculação direta
ax.plot(x, mun_mes["Direto"], marker="o", color=COR_SECUNDARIA,
        linewidth=2, markersize=4, linestyle="--", label="Só veiculação direta")

ax.axhline(mun_mes["Abrangencia"].mean(), color=COR_PRINCIPAL,
           linestyle=":", linewidth=1, alpha=0.6)
ax.axhline(mun_mes["Direto"].mean(), color=COR_SECUNDARIA,
           linestyle=":", linewidth=1, alpha=0.6)

ax.set_title("Municípios Alcançados por Mês — 2023–2026\n"
             "(veiculação direta vs abrangência real do sinal)",
             fontweight="bold")
ax.set_ylabel("Municípios únicos")
ax.legend(loc="upper right", fontsize=9)
plt.xticks(range(len(x)), x, rotation=60, ha="right", fontsize=7)
nota_rodape(ax, "Abrangência = todos os municípios no sinal das rádios que veicularam no mês")
fig.tight_layout()
salvar(fig, "12_municipios_por_mes.png")

# ── 13 Perfil de conteúdo por rádio — PALETA CORRIGIDA ───────────────────────
top_r_idx = df["Radio"].value_counts().head(TOP_N_RADIOS).index
pivot_p = (df[df["Radio"].isin(top_r_idx)]
           .groupby(["Radio","Tipo_Plot"]).size()
           .unstack(fill_value=0)
           .reindex(columns=ordem_cats, fill_value=0))
pivot_p = pivot_p.loc[:, (pivot_p > 0).any(axis=0)]
cats_presentes = [c for c in ordem_cats if c in pivot_p.columns]

n_radios = len(pivot_p); n_cats = len(cats_presentes)
bar_w = 0.7 / n_cats
x_r   = range(n_radios)

fig, ax = plt.subplots(figsize=(16, 7), facecolor="#f8f9fa")
ax.set_facecolor("white")
for i, cat in enumerate(cats_presentes):
    offset = (i - n_cats/2 + 0.5) * bar_w
    color  = PALETA_TIPO.get(cat, "#bdc3c7")
    ax.bar([xi + offset for xi in x_r], pivot_p[cat].values, bar_w * 0.92,
           color=color, label=cat, edgecolor="white", linewidth=0.3)

nomes = [r.split(" -")[0][:28] for r in pivot_p.index]
ax.set_xticks(x_r)
ax.set_xticklabels(nomes, rotation=35, ha="right", fontsize=8)
ax.set_ylabel("Veiculações", fontsize=11)
ax.set_title("Perfil de Conteúdo por Rádio (Top 10) — Histórico Total",
             fontsize=13, fontweight="bold", pad=12)
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
ax.spines[["top","right"]].set_visible(False)
handles13 = [mpatches.Patch(color=PALETA_TIPO.get(c,"#bdc3c7"), label=c) for c in cats_presentes]
ax.legend(handles=handles13, loc="upper right", fontsize=8,
          framealpha=0.9, edgecolor="#ddd", ncol=2, fancybox=True)
plt.tight_layout()
salvar(fig, "13_perfil_conteudo_por_radio.png")

# ── 14 Ciclo de vida por tipo ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
ciclo_tipo_plot = ciclo_tipo[ciclo_tipo["Veiculacoes"] >= 10]
ax.barh(ciclo_tipo_plot["Tipo"][::-1], ciclo_tipo_plot["Mediana_dias"][::-1], color=COR_PRINCIPAL)
ax.set_xlabel("Mediana de dias entre criação e veiculação")
ax.set_title("Ciclo de Vida Mediano por Tipo de Conteúdo", fontweight="bold")
nota_rodape(ax, "Tipos com mediana alta = conteúdo evergreen ou distribuição lenta")
fig.tight_layout()
salvar(fig, "14_ciclo_vida_por_tipo.png")

# ── 15 Janela de veiculação ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
dados_hist = df_ciclo[df_ciclo["Dias_Ate_Veiculacao"] <= 30]["Dias_Ate_Veiculacao"]
ax.hist(dados_hist, bins=31, range=(0,30), color=COR_SECUNDARIA, edgecolor="white")
ax.set_xlabel("Dias após a criação"); ax.set_ylabel("Número de veiculações")
ax.set_title("Quando os Conteúdos São Veiculados Após a Criação (primeiros 30 dias)", fontweight="bold")
pct_d0 = (dados_hist == 0).mean() * 100
pct_d3 = (dados_hist <= 3).mean() * 100
nota_rodape(ax, f"Dia 0: {pct_d0:.0f}% | Primeiros 3 dias: {pct_d3:.0f}% das veiculações")
fig.tight_layout()
salvar(fig, "15_janela_veiculacao.png")

# ── 16 Mapa interativo de intensidade ────────────────────────────────────────
print("\n[4.1/8] Gerando Mapa Interativo de Intensidade...")

if PLOTLY_DISPONIVEL:
    # Carrega centroides com população
    df_cent_pop = pd.read_csv(StringIO(CENTROIDES_POP_CSV))
    df_cent_pop["Cidade_norm"] = df_cent_pop["municipio"].apply(normalizar)

    # Merge alcance + população do CSV de intensidade
    mapa_int = (alcance
    .drop(columns=["lat","lon"], errors="ignore")  # remove lat/lon do merge anterior
    .merge(df_cent_pop[["Cidade_norm","lat","lon","pop"]],
           on="Cidade_norm", how="left")
    .dropna(subset=["lat","lon","pop"])
    )

    # Métricas
    mapa_int["Indice_Intensidade"] = (mapa_int["Veiculacoes"] / mapa_int["pop"] * 10_000).round(1)
    mapa_int["Audiencia_Potencial"] = (mapa_int["pop"] * TAXA_ESCUTA_RADIO).round(0).astype(int)

    q1_int   = mapa_int["Indice_Intensidade"].quantile(0.25)
    q3_int   = mapa_int["Indice_Intensidade"].quantile(0.75)
    med_int  = mapa_int["Indice_Intensidade"].median()
    vmax_cap = mapa_int["Indice_Intensidade"].quantile(0.95)

    def classificar_int(idx):
        if idx >= q3_int:  return "🟢 Alta intensidade"
        if idx >= q1_int:  return "🟡 Intensidade média"
        return                    "🔴 Baixa intensidade"

    mapa_int["Classificacao"]   = mapa_int["Indice_Intensidade"].apply(classificar_int)
    mapa_int["Veiculacoes_fmt"] = mapa_int["Veiculacoes"].apply(lambda x: f"{x:,}".replace(",","."))
    mapa_int["Populacao_fmt"]   = mapa_int["pop"].apply(lambda x: f"{x:,}".replace(",","."))
    mapa_int["Audiencia_fmt"]   = mapa_int["Audiencia_Potencial"].apply(lambda x: f"{x:,}".replace(",","."))
    mapa_int["Indice_fmt"]      = mapa_int["Indice_Intensidade"].apply(lambda x: f"{x:.1f}")
    mapa_int["Indice_cor"]      = mapa_int["Indice_Intensidade"].clip(upper=vmax_cap)

    fig_int = px.scatter_mapbox(
        mapa_int,
        lat="lat", lon="lon",
        size="pop",
        color="Indice_cor",
        hover_name="Cidade",
        hover_data={
            "lat": False, "lon": False, "pop": False, "Indice_cor": False,
            "Veiculacoes_fmt": True,
            "Populacao_fmt":   True,
            "Audiencia_fmt":   True,
            "Indice_fmt":      True,
            "Classificacao":   True,
        },
        color_continuous_scale=[
            [0.0,  "#d73027"],
            [0.35, "#fc8d59"],
            [0.5,  "#fee08b"],
            [0.65, "#91cf60"],
            [1.0,  "#1a9850"],
        ],
        range_color=[0, vmax_cap],
        size_max=50,
        zoom=6.8,
        center={"lat": -27.5, "lon": -50.5},
        mapbox_style="carto-positron",
        labels={
            "Veiculacoes_fmt": "Veiculações",
            "Populacao_fmt":   "População",
            "Audiencia_fmt":   "Audiência potencial",
            "Indice_fmt":      "Índice (/10k hab.)",
            "Classificacao":   "Classificação",
            "Indice_cor":      "Índice de intensidade",
        },
    )

    fig_int.update_layout(
        margin={"r": 0, "t": 70, "l": 0, "b": 0},
        paper_bgcolor="#f8f9fa",
        font=dict(family="Arial, sans-serif", size=13),
        title=dict(
            text=(f"<b>Intensidade de Cobertura — Rádio Alesc ({anos_validos[0]}–{anos_validos[-1]})</b><br>"
                  "<sup>Tamanho = população  ·  Cor = veiculações por 10.000 hab.  "
                  "·  Passe o mouse sobre cada cidade para detalhes</sup>"),
            x=0.5, xanchor="center",
            font=dict(size=15),
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Índice<br>(/10k hab.)", font=dict(size=11)),
            tickfont=dict(size=10),
            thickness=16, len=0.6, x=1.0,
            tickvals=[0, vmax_cap*0.25, vmax_cap*0.5, vmax_cap*0.75, vmax_cap],
            ticktext=[
                "0",
                f"{vmax_cap*0.25:.0f}",
                f"{vmax_cap*0.5:.0f} (≈mediana)",
                f"{vmax_cap*0.75:.0f}",
                f"≥{vmax_cap:.0f}",
            ],
        ),
        annotations=[dict(
            text=(f"🔴 Baixa: <{q1_int:.0f}/10k  "
                  f"🟡 Média: {q1_int:.0f}–{q3_int:.0f}/10k  "
                  f"🟢 Alta: >{q3_int:.0f}/10k  |  "
                  f"{len(mapa_int)} municípios cobertos"),
            xref="paper", yref="paper",
            x=0.5, y=-0.02,
            xanchor="center", yanchor="top",
            showarrow=False,
            font=dict(size=10, color="#555"),
        )],
    )

    caminho_int = OUTPUT_DIR / "mapa_intensidade_interativo.html"
    fig_int.write_html(
        str(caminho_int),
        include_plotlyjs="cdn",
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
            },
        },
    )
    print(f"  ✓ {caminho_int.name} — {caminho_int.stat().st_size / 1024:.0f} KB")
else:
    print("  ⚠ Mapa interativo ignorado (plotly não disponível)")

if PLOTLY_DISPONIVEL:
    print("[4.1/8] Gerando Mapa Interativo de Abrangência Real...")
    
    # 1. Identificar municípios impactados no último ano
    rads_ativas = df[df["Ano"] == anos_validos[-1]]["Radio_norm"].unique()
    cids_impactadas = set()
    for rn in rads_ativas:
        # Sede
        sede_match = df[df["Radio_norm"] == rn]["Cidade_norm"].unique()
        if len(sede_match) > 0: cids_impactadas.add(sede_match[0])
        # Abrangência
        if rn in mapa_abrangencia:
            cids_impactadas.update(mapa_abrangencia[rn])

    # 2. CONSTRUÇÃO ROBUSTA DO DATAFRAME
    # Criamos um DF temporário com as cidades e fazemos MERGE com df_cent_pop
    # (Usando df_cent_pop que você carregou no bloco de Intensidade e tem lat/lon)
    df_temp_cids = pd.DataFrame({"Cidade_norm": list(cids_impactadas)})
    
    mapa_abr = df_temp_cids.merge(
        df_cent_pop[["Cidade_norm", "lat", "lon", "pop", "municipio"]], 
        on="Cidade_norm", 
        how="inner"
    )

    if not mapa_abr.empty:
        # 3. Formatação
        mapa_abr["Populacao_fmt"] = mapa_abr["pop"].apply(lambda x: f"{x:,}".replace(",","."))
        
        # 4. Geração do Mapa com Barra de Cores para População
        fig_abr = px.scatter_mapbox(
            mapa_abr,
            lat="lat",
            lon="lon",
            size="pop",
            color="pop", # A cor agora segue a população
            hover_name="municipio",
            hover_data={
                "lat": False, "lon": False, "pop": False,
                "Populacao_fmt": True
            },
            color_continuous_scale="Viridis", 
            size_max=35,
            zoom=6.8,
            center={"lat": -27.5, "lon": -50.5},
            mapbox_style="carto-positron",
            labels={"pop": "População", "Populacao_fmt": "Habitantes"}
        )

        # Ajuste de opacidade (sem 'line' para não dar erro)
        fig_abr.update_traces(marker=dict(opacity=0.7))

        # 5. CONFIGURAÇÃO DA BARRA DIREITA (Igual ao de intensidade)
        fig_abr.update_layout(
            margin={"r": 0, "t": 70, "l": 0, "b": 0},
            coloraxis_showscale=True, # AGORA LIGAMOS A BARRA
            coloraxis_colorbar=dict(
                title=dict(text="População", font=dict(size=12)),
                thickness=15,
                len=0.5,
                yanchor="middle",
                y=0.5,
                tickformat=",", # Formato com separador de milhar
                ticksuffix=" hab."
            ),
            title=dict(
                text=f"<b>Mancha de Cobertura Territorial — Rádio Alesc ({anos_validos[-1]})</b>",
                x=0.5, xanchor="center",
                font=dict(size=16)
            )
        )

        caminho_abr = OUTPUT_DIR / "mapa_abrangencia_interativo.html"
        fig_abr.write_html(str(caminho_abr))
        print(f"  ✓ {caminho_abr.name} gerado com sucesso.")
else:
    print("  ⚠ Plotly não disponível para o mapa de abrangência.")


# ── 16 Cobertura real vs veiculação direta ───────────────────────────────────
if df_pop is not None and mapa_abrangencia:
    cob = df_pop[["Municipio_IBGE","Cidade_norm","Populacao"]].copy()
    cob["Coberto_Veiculacao"]  = cob["Cidade_norm"].isin(municipios_veiculacao)
    cob["Coberto_Abrangencia"] = cob["Cidade_norm"].isin(municipios_cobertos_real)
    cob = cob.merge(df_centroides[["Cidade_norm","lat","lon"]], on="Cidade_norm", how="left")
    cob = cob.dropna(subset=["lat","lon"])

    def categoria(row):
        if row["Coberto_Veiculacao"]:   return "Veiculação direta"
        if row["Coberto_Abrangencia"]:  return "Só abrangência"
        return "Sem cobertura"
    cob["Categoria"] = cob.apply(categoria, axis=1)

    cores_cat = {
        "Veiculação direta": COR_POSITIVO,
        "Só abrangência":    COR_PRINCIPAL,
        "Sem cobertura":     COR_ALERTA,
    }
    tamanhos  = {"Veiculação direta": 80, "Só abrangência": 40, "Sem cobertura": 20}
    alphas    = {"Veiculação direta": 0.9, "Só abrangência": 0.6, "Sem cobertura": 0.3}

    fig, ax = plt.subplots(figsize=(14, 10), facecolor="#f8f9fa")
    ax.set_facecolor("#dce8f5")
    border_lats = [-29.35,-29.10,-28.93,-28.68,-28.45,-28.20,-27.90,-27.60,
                   -27.37,-26.90,-26.76,-26.45,-26.23,-26.02,-26.02,-26.10,
                   -26.18,-26.10,-26.40,-26.35,-26.25,-26.20,-26.50,-26.35,
                   -26.25,-26.80,-27.20,-27.50,-28.00,-28.40,-28.80,-29.10,
                   -29.35,-29.35,-29.35,-29.35,-29.35,-29.35]
    border_lons = [-49.72,-49.63,-49.42,-49.12,-48.78,-48.67,-48.68,-48.55,
                   -48.40,-48.62,-48.68,-48.59,-48.64,-48.63,-49.10,-49.50,
                   -50.00,-50.30,-50.80,-51.10,-51.50,-52.00,-52.50,-53.00,
                   -53.65,-53.75,-53.85,-53.80,-54.00,-53.85,-53.50,-53.20,
                   -52.80,-52.00,-51.50,-50.80,-50.20,-49.72]
    ax.fill(border_lons, border_lats, color="#f0f4f0", alpha=0.95, zorder=1)
    ax.plot(border_lons+[border_lons[0]], border_lats+[border_lats[0]],
            color="#7a9a7a", linewidth=1.2, zorder=2)

    for cat, grp in cob.groupby("Categoria"):
        ax.scatter(grp["lon"], grp["lat"],
                   s=tamanhos[cat], color=cores_cat[cat],
                   alpha=alphas[cat], edgecolors="white", linewidths=0.4,
                   label=f"{cat} ({len(grp)})", zorder=3+list(cores_cat).index(cat))

    # Labels dos municípios sem cobertura com > 20k hab
    sem_cob_grandes = cob[(cob["Categoria"]=="Sem cobertura") & (cob["Populacao"]>20_000)]
    for _, row in sem_cob_grandes.iterrows():
        ax.annotate(row["Municipio_IBGE"], (row["lon"], row["lat"]),
                    fontsize=6.5, color=COR_ALERTA, fontweight="bold",
                    xytext=(4,4), textcoords="offset points")

    totais_cat = cob["Categoria"].value_counts()
    pop_sem = cob[cob["Categoria"]=="Sem cobertura"]["Populacao"].sum()
    ax.text(0.015, 0.985,
            f"▪ Veiculação direta: {totais_cat.get('Veiculação direta',0)} municípios\n"
            f"▪ Só abrangência: {totais_cat.get('Só abrangência',0)} municípios\n"
            f"▪ Sem cobertura: {totais_cat.get('Sem cobertura',0)} municípios\n"
            f"▪ Pop. sem cobertura: {pop_sem/1e6:.1f}M hab.",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.88, edgecolor="#ccc"))

    ax.set_xlim(-54.3, -47.8); ax.set_ylim(-29.6, -25.7)
    ax.legend(loc="lower left", fontsize=9, framealpha=0.85)
    ax.set_title("Cobertura Real da Rádio Alesc — SC\n"
                 "Verde = veiculação direta  ·  Azul = só abrangência  ·  Vermelho = sem cobertura",
                 fontsize=12, fontweight="bold", pad=10)
    nota_rodape(ax, "Abrangência = municípios no sinal de cada rádio parceira ativa")
    fig.tight_layout()
    salvar(fig, "16_cobertura_real_vs_veiculacao.png")

# ── 17 Ranking de rádios por alcance de abrangência ──────────────────────────
if mapa_abrangencia:
    top_abr = impacto_radio.head(15).copy()
    top_abr["Label"] = top_abr.apply(
        lambda r: f"{r['Radio'].split(' -')[0][:25]}\n"
                  f"({int(r['Municipios_Abrangencia'])} mun. | {int(r['Veiculacoes'])} veic.)",
        axis=1
    )

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # Painel esquerdo: impacto por abrangência
    ax = axes[0]
    bars = ax.barh(top_abr["Label"][::-1], top_abr["Impacto_Abrangencia"][::-1]/1e6,
                   color=COR_PRINCIPAL, alpha=0.85)
    ax.set_xlabel("População de abrangência (M hab.)")
    ax.set_title("Por Abrangência Real do Sinal", fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.1f}M"))
    for bar, val in zip(bars, top_abr["Impacto_Abrangencia"][::-1]/1e6):
        ax.text(bar.get_width()+0.02, bar.get_y()+bar.get_height()/2,
                f"{val:.1f}M", va="center", fontsize=7)

    # Painel direito: impacto por município sede (método antigo — para comparação)
    ax = axes[1]
    top_sede = impacto_radio.sort_values("Impacto_Sede", ascending=False).head(15)
    top_sede["Label2"] = top_sede["Radio_norm"].apply(
        lambda rn: f"{mapa_display.get(rn, rn).split(' -')[0][:25]} — {mapa_global_cidade.get(rn, '')}"
    )
    bars2 = ax.barh(top_sede["Label2"][::-1], top_sede["Impacto_Sede"][::-1]/1e6,
                    color=COR_SECUNDARIA, alpha=0.85)
    ax.set_xlabel("População da cidade sede (M hab.)")
    ax.set_title("Por Município Sede (método anterior)", fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.1f}M"))

    fig.suptitle("Top 15 Rádios por Impacto — Abrangência Real vs Município Sede",
                 fontsize=13, fontweight="bold")
    nota_rodape(axes[1], "Abrangência = pop. total de todos municípios no sinal da rádio")
    fig.tight_layout()
    salvar(fig, "17_ranking_abrangencia_vs_sede.png")

# Carregamento robusto do mapa de SC
GEOPANDAS_ATIVO = False
try:
    import geopandas as gpd
    url_sc = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/42?formato=application/vnd.geo+json&qualidade=maxima&intrarregiao=municipio"
    response = requests.get(url_sc)
    if response.status_code == 200:
        data = response.json()
        # O GeoPandas lê o dicionário JSON diretamente
        mapa_sc = gpd.GeoDataFrame.from_features(data["features"])
        # Definir o sistema de coordenadas (WGS84)
        mapa_sc.set_crs(epsg=4326, inplace=True)
        GEOPANDAS_ATIVO = True
        print("  ✓ Malha municipal de SC carregada via IBGE.")
except Exception as e:
    print(f"  ⚠ Erro ao carregar GeoPandas: {e}")

if GEOPANDAS_ATIVO and df_pop is not None:
    # 1. Preparar dados
    cob = df_pop[["Municipio_IBGE","Cidade_norm","Populacao"]].copy()
    cob["Coberto_Veiculacao"]  = cob["Cidade_norm"].isin(municipios_veiculacao)
    cob["Coberto_Abrangencia"] = cob["Cidade_norm"].isin(municipios_cobertos_real)
    
    def categoria(row):
        if row["Coberto_Veiculacao"]:   return "Veiculação direta"
        if row["Coberto_Abrangencia"]:  return "Só abrangência"
        return "Sem cobertura"
    cob["Categoria"] = cob.apply(categoria, axis=1)

    # 2. Configurar o Plot
    fig, ax = plt.subplots(figsize=(14, 10), facecolor="white")
    ax.set_facecolor("#f0f5f9") # Cor do mar/fundo

    # 3. DESENHAR O MAPA DE FUNDO (A mágica do GeoPandas)
    mapa_sc.plot(ax=ax, color="#ffffff", edgecolor="#d1d1d1", linewidth=0.5, zorder=1)
    
    # 4. PLOTAR OS PONTOS (Estilo Bolhas Proporcionais)
    cores_cat = {
        "Veiculação direta": "#27ae60", # Verde
        "Só abrangência":    "#2980b9", # Azul
        "Sem cobertura":     "#e74c3c"  # Vermelho
    }
    
    for cat in ["Sem cobertura", "Só abrangência", "Veiculação direta"]:
        grp = cob[cob["Categoria"] == cat]
        
        # Faz o merge para garantir que temos as coordenadas lat/lon
        dados_geo = grp.merge(df_centroides[["Cidade_norm", "lat", "lon"]], on="Cidade_norm")
        
        if not dados_geo.empty:
            # Calculamos o tamanho baseado na população presente neste grupo específico
            tamanhos = (dados_geo["Populacao"] / 1000) * 1.8
            tamanhos = tamanhos.clip(lower=10, upper=600)
            
            ax.scatter(
                dados_geo["lon"], dados_geo["lat"],
                s=tamanhos, # Usa os tamanhos calculados para este grupo
                color=cores_cat[cat],
                alpha=0.7,
                edgecolors="white",
                linewidths=0.5,
                label=f"{cat} ({len(grp)})",
                zorder=3 if cat == "Sem cobertura" else 4
            )

    # 5. LABELS E ESTÉTICA
    ax.axis("off") # Remove eixos de coordenadas
    
    plt.title("COBERTURA REAL DA RÁDIO ALESC", loc='left', fontsize=16, fontweight='bold', pad=10)
    ax.text(0, 1.02, "Análise de alcance territorial: Sede vs. Abrangência de Sinal", 
            transform=ax.transAxes, fontsize=10, color='#666')

    ax.legend(loc="lower right", title="Categorias", frameon=True, shadow=False)
    
    fig.tight_layout()
    salvar(fig, "16_cobertura_real_premium.png")



# ══════════════════════════════════════════════════════════════════════════════
# 6. EXPORTAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
print("\n[5/8] Exportando tabelas...")

ciclo_tipo.to_csv(OUTPUT_DIR / "ciclo_vida_por_tipo.csv", index=False)
ciclo_comercial.head(50).to_csv(OUTPUT_DIR / "comerciais_mais_longevos.csv", index=False)
zumbis.head(30).to_csv(OUTPUT_DIR / "conteudos_zumbis.csv", index=False)

df_export = df.drop(columns=["Arquivo","Hora_dt","Cidade_norm","Radio_norm","Tipo_Plot"], errors="ignore")
df_export.to_csv(OUTPUT_DIR / "dataset_consolidado.csv", index=False, encoding="utf-8-sig")
print("  ✓ dataset_consolidado.csv")

alcance.drop(columns=["Cidade_norm"], errors="ignore").sort_values(
    "Alcance_Ponderado", ascending=False
).to_excel(OUTPUT_DIR / "alcance_municipios.xlsx", index=False)
print("  ✓ alcance_municipios.xlsx")

(alcance[["Cidade","Populacao","Veiculacoes","Indice_Intensidade","Alcance_Ponderado"]]
 .drop_duplicates().sort_values("Indice_Intensidade", ascending=False)
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

# ── Relatórios estratégicos ───────────────────────────────────────────────────
print("\n[5.1/8] Gerando relatórios estratégicos...")

# Relatório 1: municípios perdidos/ganhos por ano
linhas_mun = []
for i in range(1, len(anos_validos)):
    a_ant, a_cur = anos_validos[i-1], anos_validos[i]
    cids_ant = set(df[df["Ano"]==a_ant]["Cidade_norm"].dropna().unique())
    cids_cur = set(df[df["Ano"]==a_cur]["Cidade_norm"].dropna().unique())
    mapa_ant = df[df["Ano"]==a_ant].drop_duplicates("Cidade_norm").set_index("Cidade_norm")["Cidade"].to_dict()
    mapa_cur = df[df["Ano"]==a_cur].drop_duplicates("Cidade_norm").set_index("Cidade_norm")["Cidade"].to_dict()
    for cn in sorted(cids_ant - cids_cur):
        if cn: linhas_mun.append({"Transicao": f"{a_ant}→{a_cur}", "Ano_Referencia": a_cur,
                                   "Municipio": mapa_ant.get(cn,cn), "Status": "Perdido"})
    for cn in sorted(cids_cur - cids_ant):
        if cn: linhas_mun.append({"Transicao": f"{a_ant}→{a_cur}", "Ano_Referencia": a_cur,
                                   "Municipio": mapa_cur.get(cn,cn), "Status": "Novo"})
df_municipios_movimento = pd.DataFrame(linhas_mun)
resumo_mun = (df_municipios_movimento.groupby(["Transicao","Status"]).size()
              .unstack(fill_value=0).reset_index())
df_municipios_movimento.to_csv(OUTPUT_DIR / "relatorio_municipios_movimento.csv",
                                index=False, encoding="utf-8-sig")
print("  ✓ relatorio_municipios_movimento.csv")

'''
# Relatório 2: rádios por ano
historico_radios_norm = set()
linhas_rad = []
for i, ano in enumerate(anos_validos):
    rads_norm_ano = set(df[df["Ano"]==ano]["Radio_norm"].dropna().unique())
    mapa_radio = df[df["Ano"]==ano].drop_duplicates("Radio_norm").set_index("Radio_norm")["Radio"].to_dict()
    mapa_cidade = df[df["Ano"]==ano].drop_duplicates("Radio_norm").set_index("Radio_norm")["Cidade"].to_dict()  # ← novo

    if i == 0:
        for rn in sorted(rads_norm_ano):
            linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn,rn),
                               "Cidade": mapa_cidade.get(rn,""),              # ← novo
                               "Status": "Ativa (ano base)"})
        historico_radios_norm.update(rads_norm_ano); continue

    a_ant = anos_validos[i-1]
    rads_norm_ant = set(df[df["Ano"]==a_ant]["Radio_norm"].dropna().unique())
    mapa_ant      = df[df["Ano"]==a_ant].drop_duplicates("Radio_norm").set_index("Radio_norm")["Radio"].to_dict()
    mapa_cid_ant  = df[df["Ano"]==a_ant].drop_duplicates("Radio_norm").set_index("Radio_norm")["Cidade"].to_dict()  # ← novo

    for rn in sorted(rads_norm_ant - rads_norm_ano):
        linhas_rad.append({"Ano": ano, "Radio": mapa_ant.get(rn,rn),
                           "Cidade": mapa_cid_ant.get(rn,""),                 # ← cidade do ano anterior
                           "Status": "Saiu"})
    for rn in sorted(rads_norm_ano - historico_radios_norm):
        linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn,rn),
                           "Cidade": mapa_cidade.get(rn,""),                  # ← novo
                           "Status": "Nova"})
    for rn in sorted((rads_norm_ano - rads_norm_ant) & historico_radios_norm):
        linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn,rn),
                           "Cidade": mapa_cidade.get(rn,""),                  # ← novo
                           "Status": "Retornou"})
    for rn in sorted(rads_norm_ano & rads_norm_ant):
        linhas_rad.append({"Ano": ano, "Radio": mapa_radio.get(rn,rn),
                           "Cidade": mapa_cidade.get(rn,""),                  # ← novo
                           "Status": "Persistente"})

    historico_radios_norm.update(rads_norm_ano)

df_radios_movimento = pd.DataFrame(linhas_rad)
resumo_rad = (df_radios_movimento[df_radios_movimento["Status"] != "Ativa (ano base)"]
              .groupby(["Ano","Status"]).size().unstack(fill_value=0).reset_index())
df_radios_movimento.to_csv(OUTPUT_DIR / "relatorio_radios_movimento.csv",
                            index=False, encoding="utf-8-sig")
print("  ✓ relatorio_radios_movimento.csv")
'''

# Relatório 2: rádios por ano


historico_radios_norm = set()
linhas_rad = []
for i, ano in enumerate(anos_validos):
    rads_norm_ano = set(df[df["Ano"]==ano]["Radio_norm"].dropna().unique())
    mapa_radio    = (df[df["Ano"]==ano].drop_duplicates("Radio_norm")
                     .set_index("Radio_norm")["Radio"].to_dict())

    if i == 0:
        for rn in sorted(rads_norm_ano):
            linhas_rad.append({
                "Ano":    ano,
                "Radio":  mapa_radio.get(rn, rn),
                "Cidade": mapa_global_cidade.get(rn, ""),
                "Status": "Ativa (ano base)"
            })
        historico_radios_norm.update(rads_norm_ano)
        continue

    a_ant         = anos_validos[i-1]
    rads_norm_ant = set(df[df["Ano"]==a_ant]["Radio_norm"].dropna().unique())
    mapa_ant      = (df[df["Ano"]==a_ant].drop_duplicates("Radio_norm")
                     .set_index("Radio_norm")["Radio"].to_dict())

    for rn in sorted(rads_norm_ant - rads_norm_ano):
        linhas_rad.append({
            "Ano":    ano,
            "Radio":  mapa_ant.get(rn, rn),
            "Cidade": mapa_global_cidade.get(rn, ""),
            "Status": "Saiu"
        })
    for rn in sorted(rads_norm_ano - historico_radios_norm):
        linhas_rad.append({
            "Ano":    ano,
            "Radio":  mapa_radio.get(rn, rn),
            "Cidade": mapa_global_cidade.get(rn, ""),
            "Status": "Nova"
        })
    for rn in sorted((rads_norm_ano - rads_norm_ant) & historico_radios_norm):
        linhas_rad.append({
            "Ano":    ano,
            "Radio":  mapa_radio.get(rn, rn),
            "Cidade": mapa_global_cidade.get(rn, ""),
            "Status": "Retornou"
        })
    for rn in sorted(rads_norm_ano & rads_norm_ant):
        linhas_rad.append({
            "Ano":    ano,
            "Radio":  mapa_radio.get(rn, rn),
            "Cidade": mapa_global_cidade.get(rn, ""),
            "Status": "Persistente"
        })

    historico_radios_norm.update(rads_norm_ano)

df_radios_movimento = pd.DataFrame(linhas_rad)
resumo_rad = (df_radios_movimento[df_radios_movimento["Status"] != "Ativa (ano base)"]
              .groupby(["Ano","Status"]).size().unstack(fill_value=0).reset_index())
df_radios_movimento.to_csv(OUTPUT_DIR / "relatorio_radios_movimento.csv",
                            index=False, encoding="utf-8-sig")
print("  ✓ relatorio_radios_movimento.csv")

# Relatório 3: população coberta por ano
# Metodologia: veiculação direta + abrangência de sinal (mesma base de cobertura_por_ano.csv)
linhas_pop = []
for ano in anos_validos:
    df_ano        = df[df["Ano"] == ano]
    rads_ano      = set(df_ano["Radio_norm"].dropna().unique())
    cids_diretas  = set(df_ano["Cidade_norm"].dropna().unique())
    cids_abrang   = set()
    for rn in rads_ano:
        if rn in mapa_abrangencia:
            cids_abrang.update(mapa_abrangencia[rn])
    cids_ano      = cids_diretas | cids_abrang
    n_cids        = len([c for c in cids_ano if c])
    pop_coberta   = df_pop[df_pop["Cidade_norm"].isin(cids_ano)]["Populacao"].sum() if df_pop is not None else n_cids * 12_000
    pct_sc        = pop_coberta / POP_SC_TOTAL * 100
    linhas_pop.append({
        "Ano": ano, "Municipios_Cobertos": n_cids,
        "Pop_Coberta": int(pop_coberta),
        "Audiencia_Potencial": int(pop_coberta * TAXA_ESCUTA_RADIO),
        "Pct_Pop_SC": round(pct_sc, 2),
        "Pct_Audiencia_SC": round(pop_coberta * TAXA_ESCUTA_RADIO / POP_SC_TOTAL * 100, 2),
        "Pop_SC_Total": POP_SC_TOTAL,
        "Pop_Nao_Coberta": POP_SC_TOTAL - int(pop_coberta),
        "Ano_Parcial": "sim" if ano > ultimo_ano_completo else "não",
    })
df_pop_ano = pd.DataFrame(linhas_pop)
df_pop_ano.to_csv(OUTPUT_DIR / "relatorio_populacao_por_ano.csv", index=False, encoding="utf-8-sig")
print("  ✓ relatorio_populacao_por_ano.csv")

# ══════════════════════════════════════════════════════════════════════════════
# 7. RELATÓRIO ANALÍTICO
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
for ano in anos_validos:
    linhas.append(f"  {ano}: {(df['Ano']==ano).sum():,} veiculações")
linhas += [
    f"Rádios parceiras (histórico total): {df['Radio'].nunique()}  |  Ativas em {anos_validos[-1]}: {df[df['Ano']==anos_validos[-1]]['Radio'].nunique()}",
    f"Municípios com veiculação direta:   {df['Cidade'].nunique()} de 295 em SC (histórico total)",
    f"Tipo mais veiculado:        {tipo_count.idxmax()} ({tipo_count.max():,})",
    "",
    "── COBERTURA TERRITORIAL (municípios sede + abrangência de sinal) ──────────",
    "  Nota: inclui todos os municípios no raio de sinal das rádios parceiras.",
    "  Para veiculação direta apenas, ver seção 'Dinâmica de Cobertura'.",
]
for _, row in cobertura_ano.iterrows():
    ano_label = f"{int(row['Ano'])}"
    if int(row['Ano']) == anos_validos[-1]:
        mes_max = df[df['Ano'] == anos_validos[-1]]['Mes'].max()
        ano_label += f" (jan–{mes_max:02d})"
    linha = f"  {ano_label}: {int(row['Municipios_Alcancados'])} municípios"
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
    continuas   = ((fidelidade["Taxa_Fidelidade"]==100) & (fidelidade["Anos_Ativo"]>=2)).sum()
    irregulares = ((fidelidade["Taxa_Fidelidade"]<75)  & (fidelidade["Anos_Ativo"]>=2)).sum()
    linhas += [f"  Rádios com histórico ininterrupto (≥2 anos, 100% dos anos ativos): {continuas}",
               f"  Rádios com presença irregular (<75%, ≥2 anos possíveis):           {irregulares}"]

if not df_churn.empty:
    # Exclui o último ano se for parcial (menos de 12 meses de dados)
    meses_ultimo_ano = df[df["Ano"] == anos_validos[-1]]["Mes"].nunique()
    churn_anos_completos = df_churn[df_churn["Ano"] != anos_validos[-1]] if meses_ultimo_ano < 12 else df_churn
    if not churn_anos_completos.empty:
        ano_mais_perdas = churn_anos_completos.loc[churn_anos_completos["Saidas"].idxmin(), "Ano"]
        linhas.append(f"  Ano com mais saídas de parceiros: {ano_mais_perdas} (excluído {anos_validos[-1]}, ano parcial)")

if not lacunas.empty:
    linhas += ["", f"── LACUNAS ESTRATÉGICAS ({len(lacunas)} cidades >{LIMIAR_LACUNA//1000}k hab.) ──"]
    for _, row in lacunas.head(8).iterrows():
        linhas.append(f"  → {row['Municipio_IBGE']}: {row['Populacao']:,} hab.")

# Índice de Intensidade
intensidade   = alcance[["Cidade","Populacao","Veiculacoes","Indice_Intensidade"]].copy()
intensidade   = intensidade[intensidade["Populacao"] > 0]
top_intens    = intensidade.nlargest(8, "Indice_Intensidade")
bottom_intens = intensidade[intensidade["Veiculacoes"] >= 5].nsmallest(8, "Indice_Intensidade")
linhas += ["", "── ÍNDICE DE INTENSIDADE (veiculações/10k hab.) ─────────────",
           "  Municípios com MAIOR intensidade (possível saturação):"]
for _, row in top_intens.iterrows():
    linhas.append(f"    {row['Cidade']:<30} {row['Indice_Intensidade']:>8.1f} "
                  f"({int(row['Veiculacoes'])} veic. / {int(row['Populacao']):,} hab.)")
linhas += ["", "  Municípios com MENOR intensidade (potencial subatendido):"]
for _, row in bottom_intens.iterrows():
    linhas.append(f"    {row['Cidade']:<30} {row['Indice_Intensidade']:>8.1f} "
                  f"({int(row['Veiculacoes'])} veic. / {int(row['Populacao']):,} hab.)")

# Dinâmica de cobertura
secao_extra = ["", "── DINÂMICA DE COBERTURA (veiculação direta — sem abrangência) ──────────────",
               "  Municípios: entradas e saídas por transição de ano"]
for _, row in resumo_mun.iterrows():
    perdidos = int(row.get("Perdido", 0)); novos = int(row.get("Novo", 0))
    saldo = novos - perdidos; sinal = "+" if saldo >= 0 else ""
    secao_extra.append(f"    {row['Transicao']}: -{perdidos} perdidos, +{novos} novos (saldo {sinal}{saldo})")
secao_extra += ["", "  Rádios: movimentação e taxa de retenção por ano"]
for ano in anos_validos[1:]:
    saiu_n = safe_get(resumo_rad, ano, "Saiu"); nova_n = safe_get(resumo_rad, ano, "Nova")
    ret_n  = safe_get(resumo_rad, ano, "Retornou"); pers_n = safe_get(resumo_rad, ano, "Persistente")
    ativas = df[df["Ano"]==ano]["Radio"].nunique()
    a_ant  = anos_validos[anos_validos.index(ano)-1]
    ant_tot = df[df["Ano"]==a_ant]["Radio"].nunique()
    retencao = f"{pers_n/ant_tot*100:.1f}%" if ant_tot > 0 else "—"
    meses_ano = df[df["Ano"]==ano]["Mes"].nunique()
    sufixo = f" ⚠ ano parcial ({meses_ano} meses)" if meses_ano < 12 else ""
    secao_extra.append(f"    {ano}: {saiu_n} saíram | {nova_n} novas | {ret_n} retornaram | "
                       f"{pers_n} persistentes | retenção {retencao} | {ativas} ativas{sufixo}")
secao_extra += ["", "  População coberta por ano (municípios únicos × pop. IBGE 2021)"]
for _, row in df_pop_ano.iterrows():
    secao_extra.append(f"    {int(row['Ano'])}: {int(row['Municipios_Cobertos'])} municípios — "
                       f"{int(row['Pop_Coberta']):,} hab. ({row['Pct_Pop_SC']:.1f}% de SC) | "
                       f"audiência potencial: {int(row['Audiencia_Potencial']):,} pessoas")

linhas += secao_extra

linhas += [
    "",
    "── FRASES PRONTAS PARA APRESENTAÇÃO ────────────────────────",
    f"  'A Rádio Alesc distribuiu {len(df):,} veiculações entre {anos_validos[0]} e {anos_validos[-1]},'",
]
if "Municipios_Alcancados" in cobertura_ano.columns:
    mun_pico = int(cobertura_ano["Municipios_Alcancados"].max())
    ano_pico = int(cobertura_ano.loc[cobertura_ano["Municipios_Alcancados"].idxmax(), "Ano"])
    linhas.append(f"  'alcançando até {mun_pico} municípios catarinenses (pico em {ano_pico}, incluindo abrangência de sinal).'")
else:
    linhas.append(f"  'alcançando {df['Cidade'].nunique()} municípios catarinenses (veiculação direta).'")
if "Pct_Pop_SC" in cobertura_ano.columns:
    meses_ultimo = df[df["Ano"] == anos_validos[-1]]["Mes"].nunique()
    ref = (cobertura_ano[cobertura_ano["Ano"] != anos_validos[-1]].iloc[-1]
           if meses_ultimo < 12 else cobertura_ano.iloc[-1])
    linhas.append(f"  'Em {int(ref['Ano'])}, a programação alcançou municípios onde vivem "
                  f"{ref['Pct_Pop_SC']:.1f}% dos catarinenses.'")
if not lacunas.empty:
    linhas.append(f"  'Há {len(lacunas)} cidades com mais de {LIMIAR_LACUNA//1000} mil habitantes "
                  "ainda sem cobertura — oportunidade concreta de expansão.'")
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
print(f"  Gráficos: 15 | Tabelas: 12 | Relatório: relatorio_analitico.txt")
print(f"  Cache IBGE: {CACHE_DIR}/")
print(f"  Outputs:    {OUTPUT_DIR}/\n")