import pandas as pd

from app.services.feature_engineering import (
    generar_features
)

from app.services.predictor import (
    predecir
)

from app.services.storage_service import (
    obtener_excel
)

from app.services.data_cleaning import (
    limpiar_dataframe
)

# ==========================================
# PREDICCIÓN NORMAL
# ==========================================
async def procesar_excel(session_id):

    df = obtener_excel(session_id)

    if df is None:

        return []

    df = limpiar_dataframe(df)

    # Solo filas reales
    df = df[df["casos"].notna()]

    # Fecha
    df["fecha"] = pd.to_datetime(
        df["ano"].astype(str)
        + "-W"
        + df["semana"].astype(str)
        + "-1",
        format="%Y-W%W-%w"
    )

    # Ordenar
    df = df.sort_values([
        "ubigeo",
        "fecha"
    ])

    # Features
    df = generar_features(df)

    # Eliminar NaN
    df = df.dropna()

    # Predicción
    predicciones = predecir(df)

    resultados = []

    for i, pred in enumerate(predicciones):

        fila = df.iloc[i]

        resultados.append({

            "ubigeo": int(fila["ubigeo"]),

            "provincia": fila["provincia"],

            "distrito": fila["distrito"],

            "ano": int(fila["ano"]),

            "semana": int(fila["semana"]),

            "casos_reales": int(fila["casos"]),

            "prediccion": round(float(pred), 2)
        })

    return resultados

# ==========================================
# PREDICCIÓN FUTURA
# ==========================================
async def predecir_futuro(
    session_id,
    semanas_futuras=4
):

    df = obtener_excel(session_id)

    if df is None:

        return []

    df = limpiar_dataframe(df)

    # Solo filas con casos reales
    df_train = df[df["casos"].notna()].copy()

    # Fecha
    df_train["fecha"] = pd.to_datetime(
        df_train["ano"].astype(str)
        + "-W"
        + df_train["semana"].astype(str)
        + "-1",
        format="%Y-W%W-%w"
    )

    # Ordenar
    df_train = df_train.sort_values([
        "ubigeo",
        "fecha"
    ])

    resultados = []

    # ======================================
    # POR UBIGEO
    # ======================================
    for ubigeo in df_train["ubigeo"].unique():

        df_zone = df_train[
            df_train["ubigeo"] == ubigeo
        ].copy()

        provincia = (
            df_zone.iloc[-1]["provincia"]
        )

        distrito = (
            df_zone.iloc[-1]["distrito"]
        )

        for _ in range(semanas_futuras):

            ultima = df_zone.iloc[-1].copy()

            nueva_semana = int(
                ultima["semana"]
            ) + 1

            nuevo_ano = int(
                ultima["ano"]
            )

            if nueva_semana > 52:

                nueva_semana = 1
                nuevo_ano += 1

            nueva = ultima.copy()

            nueva["semana"] = nueva_semana
            nueva["ano"] = nuevo_ano

            # ==================================
            # FEATURE ENGINEERING
            # ==================================
            temp_df = pd.concat([
                df_zone,
                pd.DataFrame([nueva])
            ])

            temp_df = generar_features(
                temp_df
            )

            fila_pred = (
                temp_df
                .tail(1)
                .fillna(0)
            )

            # ==================================
            # PREDECIR
            # ==================================
            pred = predecir(
                fila_pred
            )[0]

            # ==================================
            # ACTUALIZAR CASOS
            # ==================================
            nueva["casos"] = pred

            df_zone = pd.concat([
                df_zone,
                pd.DataFrame([nueva])
            ])

            resultados.append({

                "ubigeo": int(ubigeo),

                "provincia": provincia,

                "distrito": distrito,

                "ano": nuevo_ano,

                "semana": nueva_semana,

                "prediccion": round(
                    float(pred),
                    2
                )
            })

    return resultados

# ==========================================
# FILTRO POR DISTRITO
# ==========================================
async def predecir_por_distrito(
    session_id,
    distrito,
    semanas
):

    resultados = await predecir_futuro(
        session_id,
        semanas
    )

    resultados = [

        x for x in resultados

        if x["distrito"].upper()
        ==
        distrito.upper()
    ]

    return resultados

# ==========================================
# FILTRO POR PROVINCIA
# ==========================================
async def predecir_por_provincia(
    session_id,
    provincia,
    semanas
):

    resultados = await predecir_futuro(
        session_id,
        semanas
    )

    resultados = [

        x for x in resultados

        if x["provincia"].upper()
        ==
        provincia.upper()
    ]

    return resultados