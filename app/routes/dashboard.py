from fastapi import APIRouter, UploadFile, File

from app.services.dashboard_service import (
    resumen_dashboard,
    top_distritos,
    heatmap_data
)
from app.services.excel_service import predecir_futuro

router = APIRouter()

# ==========================================
# TOP DISTRITOS
# ==========================================
@router.post("/top-districts")
async def top_top_districts(
    session_id: str
):

    resultados = await predecir_futuro(
        session_id,
        4
    )

    top = sorted(
        resultados,
        key=lambda x: x["prediccion"],
        reverse=True
    )[:10]

    return top