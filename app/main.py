from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.predict import router as predict_router
from app.routes.catalog import router as catalog_router
from app.routes.dashboard import router as dashboard_router
from database import predicciones_collection
from datetime import datetime

app = FastAPI()

# ==========================================
# CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
app.include_router(catalog_router)
app.include_router(dashboard_router)
app.include_router(upload_router)

@app.get("/")
def root():
    return {
        "message": "API Dengue funcionando"
    }