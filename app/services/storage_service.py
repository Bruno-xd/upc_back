import pandas as pd

from io import BytesIO

from app.services.data_cleaning import (
    limpiar_dataframe
)

# ==========================================
# MEMORIA TEMPORAL
# ==========================================
storage = {}

# ==========================================
# GUARDAR EXCEL
# ==========================================
async def guardar_excel(
    session_id,
    file
):

    contents = await file.read()

    df = pd.read_excel(
        BytesIO(contents),
        sheet_name="Distrito"
    )

    # ======================================
    # LIMPIAR DATAFRAME
    # ======================================
    df = limpiar_dataframe(df)

    # ======================================
    # GUARDAR EN MEMORIA
    # ======================================
    storage[session_id] = df

# ==========================================
# OBTENER EXCEL
# ==========================================
def obtener_excel(
    session_id
):

    return storage.get(session_id)