import joblib
import numpy as np

# ==========================================
# CARGAR MODELO
# ==========================================
model = joblib.load(
    "app/models/xgboost_dengue.pkl"
)

scaler_X = joblib.load(
    "app/models/scaler_X.pkl"
)

scaler_y = joblib.load(
    "app/models/scaler_y.pkl"
)

features = joblib.load(
    "app/models/features.pkl"
)

# ==========================================
# NOMBRES AMIGABLES
# ==========================================
NOMBRES_VARIABLES = {

    "casos_roll4": "Promedio de casos de las últimas 4 semanas",

    "casos_lag1": "Casos reportados la semana anterior",

    "casos_lag2": "Casos reportados hace 2 semanas",

    "casos_lag3": "Casos reportados hace 3 semanas",

    "casos_lag4": "Casos reportados hace 4 semanas",

    "casos_diff": "Variación de casos respecto a la semana anterior",

    "ptot": "Precipitación acumulada",

    "ptot_lag1": "Precipitación de la semana anterior",

    "ptot_lag2": "Precipitación de hace 2 semanas",

    "ptot_lag3": "Precipitación de hace 3 semanas",

    "ptot_roll4": "Promedio de precipitación de las últimas 4 semanas",

    "ptot_diff": "Variación de precipitación",

    "tmean": "Temperatura media",

    "tmean_lag1": "Temperatura media de la semana anterior",

    "tmean_lag2": "Temperatura media de hace 2 semanas",

    "tmean_anom": "Anomalía de temperatura media",

    "tmax": "Temperatura máxima",

    "tmin": "Temperatura mínima",

    "humr": "Humedad relativa",

    "semana_sin": "Patrón estacional semanal (seno)",

    "semana_cos": "Patrón estacional semanal (coseno)",

    "temp_x_lluvia": "Interacción entre temperatura y precipitación",

    "ubigeo": "Ubicación geográfica (UBIGEO)",

    "ptot_anom": "Anomalía de precipitación"
}

# ==========================================
# PREDECIR
# ==========================================
def predecir(df_features):

    X = df_features[features]

    X_scaled = scaler_X.transform(X)

    y_pred = model.predict(X_scaled)

    y_pred_scaled = scaler_y.inverse_transform(
        y_pred.reshape(-1, 1)
    )

    y_pred_inv = np.expm1(
        y_pred_scaled
    )

    return y_pred_inv.flatten()

# ==========================================
# IMPORTANCIA DE VARIABLES
# ==========================================
def obtener_importancia_variables():

    importancias = []

    for feature, importancia in zip(
        features,
        model.feature_importances_
    ):

        importancias.append({

            "variable": feature,

            "nombre": NOMBRES_VARIABLES.get(
                feature,
                feature
            ),

            "importancia": round(
                float(importancia),
                4
            )
        })

    importancias.sort(
        key=lambda x: x["importancia"],
        reverse=True
    )

    return {

        "interpretacion":
        "El modelo se apoya principalmente en el comportamiento reciente de los casos de dengue. Las variables más influyentes corresponden al historial epidemiológico de semanas anteriores y a los promedios recientes de casos.",

        "importancias": importancias
    }