from fastapi import APIRouter

from app.api.routes_chat import router as chat_router
from app.api.routes_health import router as health_router
from app.api.routes_upload import router as upload_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(upload_router, prefix="/documents", tags=["documents"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
