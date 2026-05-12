import pandas as pd

# ==========================================
# LIMPIAR DATAFRAME
# ==========================================
def limpiar_dataframe(df):

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )

    cols = [
        "tmean","tmax","tmin",
        "humr","ptot",
        "tmean_clima",
        "tmax_clima",
        "tmin_clima",
        "humr_clima",
        "ptot_clima",
        "casos"
    ]

    for col in cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df["ubigeo"] = pd.to_numeric(
        df["ubigeo"],
        errors="coerce"
    )

    return df