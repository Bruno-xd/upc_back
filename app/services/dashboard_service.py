from app.services.excel_service import (
    predecir_futuro
)

# ==========================================
# SUMMARY
# ==========================================
async def resumen_dashboard(
    file,
    semanas
):

    resultados = await predecir_futuro(
        file,
        semanas
    )

    total = sum(
        x["prediccion"]
        for x in resultados
    )

    max_item = max(
        resultados,
        key=lambda x: x["prediccion"]
    )

    return {

        "total_predicciones": round(total, 2),

        "max_prediccion": max_item[
            "prediccion"
        ],

        "distrito_critico": max_item[
            "distrito"
        ],

        "provincia_critica": max_item[
            "provincia"
        ]
    }

# ==========================================
# TOP DISTRITOS
# ==========================================
async def top_distritos(
    file,
    semanas,
    top_n
):

    resultados = await predecir_futuro(
        file,
        semanas
    )

    resultados = sorted(
        resultados,
        key=lambda x: x["prediccion"],
        reverse=True
    )

    return resultados[:top_n]

# ==========================================
# HEATMAP
# ==========================================
async def heatmap_data(
    file,
    semanas
):

    resultados = await predecir_futuro(
        file,
        semanas
    )

    heatmap = []

    for item in resultados:

        heatmap.append({

            "ubigeo": item["ubigeo"],

            "provincia": item["provincia"],

            "distrito": item["distrito"],

            "prediccion": item["prediccion"]
        })

    return heatmap