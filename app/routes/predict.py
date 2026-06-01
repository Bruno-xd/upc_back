from fastapi import APIRouter

from datetime import datetime

from pydantic import EmailStr

from app.services.pdf_service import generar_pdf_reporte

from app.services.email_service import enviar_alerta

from app.database import (
    predicciones_collection
)

from app.services.excel_service import (
    procesar_excel,
    predecir_futuro,
    predecir_por_distrito,
    predecir_por_provincia
)

from app.services.storage_service import (
    obtener_excel
)

from app.services.predictor import (
    obtener_importancia_variables
)

router = APIRouter()

# ==========================================
# PREDICT FILE
# ==========================================
@router.post("/predict-file")
async def predict_file(
    session_id: str
):

    resultados = await procesar_excel(
        session_id
    )

    return {

        "total_predicciones": len(resultados),

        "predicciones": resultados
    }

# ==========================================
# FUTURO
# ==========================================
@router.post("/predict-future")
async def predict_future(
    session_id: str,
    correo: EmailStr,
    semanas: int = 4
):

    resultados = await predecir_futuro(
        session_id,
        semanas
    )

    # ======================================
    # VARIABLES ALERTA
    # ======================================
    alertas = []

    # ======================================
    # GUARDAR EN MONGO
    # ======================================
    for item in resultados:

        prediccion = float(
            item.get("prediccion", 0)
        )

        predicciones_collection.insert_one({

            "tipo": "prediccion_futura",

            "provincia": item.get("provincia"),
            "distrito": item.get("distrito"),

            "ano": item.get("ano"),
            "semana": item.get("semana"),

            "prediccion": prediccion,

            "fecha_generacion": datetime.now()
        })

        # ======================================
        # DETECTAR ALERTAS
        # ======================================
        if prediccion > 60:

            alertas.append({

                "provincia": item.get("provincia"),
                "distrito": item.get("distrito"),
                "semana": item.get("semana"),
                "ano": item.get("ano"),
                "prediccion": round(prediccion, 2)

            })

    # ======================================
    # GENERAR PDF
    # ======================================
    pdf_path = generar_pdf_reporte(
        resultados=resultados,
        alertas=alertas
    )
    # ======================================
    # ENVIAR UN SOLO CORREO
    # ======================================
    if len(alertas) > 0:

        cuerpo = """
        ALERTA TEMPRANA DE DENGUE

        Se detectaron posibles riesgos altos de dengue:

        """

        for alerta in alertas:

            cuerpo += f"""

            Provincia: {alerta['provincia']}
            Distrito: {alerta['distrito']}
            Año: {alerta['ano']}
            Semana: {alerta['semana']}
            Casos estimados: {alerta['prediccion']}

            ------------------------
            """

        enviar_alerta(
            destinatario=str(correo),
            asunto="⚠️ Reporte de Riesgo de Dengue",
            mensaje=cuerpo,
            archivo_adjunto=pdf_path
        )

    else:

        cuerpo = f"""
        REPORTE DE PREDICCIÓN DE DENGUE

        La predicción se ejecutó correctamente.

        Total de predicciones generadas: {len(resultados)}

        No se detectaron zonas con riesgo alto de dengue
        para el período analizado.
        """

        enviar_alerta(
            destinatario=str(correo),
            asunto="✅ Reporte de Predicción de Dengue",
            mensaje=cuerpo,
            archivo_adjunto=pdf_path
        )

    return {
        "total_predicciones": len(resultados),
        "total_alertas": len(alertas),
        "predicciones_futuras": resultados
    }

# ==========================================
# POR DISTRITO
# ==========================================
@router.post("/predict-by-district")
async def predict_by_district(
    session_id: str,
    distrito: str,
    semanas: int = 4
):

    resultados = await predecir_por_distrito(
        session_id,
        distrito,
        semanas
    )

    # ======================================
    # GUARDAR EN MONGO
    # ======================================
    for item in resultados:

        predicciones_collection.insert_one({

            "tipo": "prediccion_distrito",

            "provincia": item.get("provincia"),
            "distrito": item.get("distrito"),

            "ano": item.get("ano"),
            "semana": item.get("semana"),

            "prediccion": float(
                item.get("prediccion", 0)
            ),

            "fecha_generacion": datetime.now()
        })

    return resultados

# ==========================================
# POR PROVINCIA
# ==========================================
@router.post("/predict-by-province")
async def predict_by_province(
    session_id: str,
    provincia: str,
    semanas: int = 4
):

    resultados = await predecir_por_provincia(
        session_id,
        provincia,
        semanas
    )

    # ======================================
    # GUARDAR EN MONGO
    # ======================================
    for item in resultados:

        predicciones_collection.insert_one({

            "tipo": "prediccion_provincia",

            "provincia": item.get("provincia"),
            "distrito": item.get("distrito"),

            "ano": item.get("ano"),
            "semana": item.get("semana"),

            "prediccion": float(
                item.get("prediccion", 0)
            ),

            "fecha_generacion": datetime.now()
        })

    return resultados

# ==========================================
# LISTA PROVINCIAS
# ==========================================
@router.get("/provinces")
async def get_provinces(
    session_id: str
):

    df = obtener_excel(session_id)

    provincias = sorted(

        df["provincia"]
        .dropna()
        .unique()
        .tolist()
    )

    return provincias

# ==========================================
# LISTA DISTRITOS
# ==========================================
@router.get("/districts")
async def get_districts(
    session_id: str,
    provincia: str
):

    df = obtener_excel(session_id)

    df = df[
        df["provincia"]
        .str.upper()
        ==
        provincia.upper()
    ]

    distritos = sorted(

        df["distrito"]
        .dropna()
        .unique()
        .tolist()
    )

    return distritos

# ==========================================
# IMPORTANCIA DE VARIABLES
# ==========================================
@router.get("/feature-importance")
async def feature_importance():

    return {
        "importancias": obtener_importancia_variables()
    }