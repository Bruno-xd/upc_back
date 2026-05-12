import numpy as np

# ==========================================
# FEATURE ENGINEERING
# ==========================================
def generar_features(df):

    # ==============================
    # ANOMALÍAS
    # ==============================
    df["tmean_anom"] = (
        df["tmean"]
        - df["tmean_clima"]
    )

    df["ptot_anom"] = (
        df["ptot"]
        - df["ptot_clima"]
    )

    # ==============================
    # ESTACIONALIDAD
    # ==============================
    df["semana_sin"] = np.sin(
        2 * np.pi * df["semana"] / 52
    )

    df["semana_cos"] = np.cos(
        2 * np.pi * df["semana"] / 52
    )

    # ==============================
    # GROUP
    # ==============================
    group_cols = ["ubigeo"]

    # ==============================
    # LAGS
    # ==============================
    for lag in [1,2,3,4]:

        df[f"casos_lag{lag}"] = (
            df.groupby(group_cols)["casos"]
            .shift(lag)
        )

        df[f"ptot_lag{lag}"] = (
            df.groupby(group_cols)["ptot"]
            .shift(lag)
        )

        df[f"tmean_lag{lag}"] = (
            df.groupby(group_cols)["tmean"]
            .shift(lag)
        )

    # ==============================
    # ROLLING
    # ==============================
    df["casos_roll4"] = (
        df.groupby(group_cols)["casos"]
        .transform(
            lambda x: x.rolling(4).mean()
        )
    )

    df["ptot_roll4"] = (
        df.groupby(group_cols)["ptot"]
        .transform(
            lambda x: x.rolling(4).mean()
        )
    )

    # ==============================
    # DIFF
    # ==============================
    df["casos_diff"] = (
        df.groupby(group_cols)["casos"]
        .diff()
    )

    df["ptot_diff"] = (
        df.groupby(group_cols)["ptot"]
        .diff()
    )

    # ==============================
    # INTERACCIÓN
    # ==============================
    df["temp_x_lluvia"] = (
        df["tmean"] * df["ptot"]
    )

    return df