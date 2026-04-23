import pandas as pd
import unicodedata
import re
from pathlib import Path

def normalizar_radio(texto):
    if pd.isna(texto): return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r'\s+', ' ', texto)
    return texto

# Como ficam as duas Meninas após normalização
print("Menina 100.5:", normalizar_radio("Menina - FM (100.5)"))
print("Menina 97.5: ", normalizar_radio("Menina - FM (97.5)"))

# Como aparecem nos xlsx
for arq in sorted(Path("data").glob("*.xlsx")):
    tmp = pd.read_excel(arq, header=None)
    if str(tmp.iloc[0,1]).strip().lower() == "data":
        tmp = tmp.iloc[2:].reset_index(drop=True)
    tmp.columns = ["Identificador","Data","Hora","Radio","Cidade_UF","Peca","Comercial"][:len(tmp.columns)]
    mask = tmp["Radio"].astype(str).str.lower().str.contains("menina", na=False)
    if mask.any():
        for r in tmp[mask]["Radio"].unique():
            print(f"  Nos dados: '{r}' → norm: '{normalizar_radio(r)}'")