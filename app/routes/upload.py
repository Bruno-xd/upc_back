from fastapi import APIRouter, UploadFile, File
import uuid

from app.services.storage_service import (
    guardar_excel
)

router = APIRouter()

# ==========================================
# UPLOAD EXCEL
# ==========================================
@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...)
):

    session_id = str(uuid.uuid4())

    await guardar_excel(
        session_id,
        file
    )

    return {

        "message": "Excel cargado correctamente",

        "session_id": session_id
    }