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
# PREDECIR
# ==========================================
def predecir(df_features):

    # Mantener EXACTAMENTE
    # las mismas columnas del entrenamiento
    X = df_features[features]

    # Escalar normal
    X_scaled = scaler_X.transform(X)

    # Predicción
    y_pred = model.predict(X_scaled)

    # Invertir escala
    y_pred_scaled = scaler_y.inverse_transform(
        y_pred.reshape(-1,1)
    )

    # Invertir log
    y_pred_inv = np.expm1(
        y_pred_scaled
    )

    return y_pred_inv.flatten()