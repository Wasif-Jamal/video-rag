from fastapi import APIRouter
from app.routes import video_upload

api_router = APIRouter()

api_router.include_router(video_upload.router)
