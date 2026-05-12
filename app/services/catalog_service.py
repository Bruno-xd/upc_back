import pandas as pd
from io import BytesIO

# ==========================================
# PROVINCIAS
# ==========================================
async def obtener_provincias(file):

    contents = await file.read()

    df = pd.read_excel(
        BytesIO(contents),
        sheet_name="Distrito"
    )

    provincias = sorted(
        df["Provincia"]
        .dropna()
        .unique()
        .tolist()
    )

    return provincias

# ==========================================
# DISTRITOS
# ==========================================
async def obtener_distritos(
    file,
    provincia=None
):

    contents = await file.read()

    df = pd.read_excel(
        BytesIO(contents),
        sheet_name="Distrito"
    )

    if provincia:

        df = df[
            df["Provincia"]
            .str.upper()
            ==
            provincia.upper()
        ]

    distritos = sorted(
        df["Distrito"]
        .dropna()
        .unique()
        .tolist()
    )

    return distritos