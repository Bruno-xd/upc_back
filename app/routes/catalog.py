from fastapi import APIRouter, UploadFile, File

from app.services.catalog_service import (
    obtener_provincias,
    obtener_distritos
)

router = APIRouter()

