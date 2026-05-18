from fastapi import APIRouter
from app.routes import video_ingestion

api_router = APIRouter()

api_router.include_router(video_ingestion.router)
