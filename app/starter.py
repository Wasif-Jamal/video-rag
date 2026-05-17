from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.routes.router import api_router
import logging

# Simple logger for now, can be expanded to match pdf-rag's log_config later if requested.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppStarter:
    """
    Factory class to bootstrap the FastAPI application using lifespan.
    """
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """
        Handles application startup and shutdown events.
        """
        logger.info("Starting Video RAG Backend initialization...")
        # Future initialization for vector stores, models, etc. will go here.
        yield
        logger.info("Shutting down Video RAG Backend...")

    def __init__(self):
        self.app = FastAPI(
            title="Video RAG Backend",
            description="Production-style Video RAG system with Lifespan support.",
            version="0.1.0",
            lifespan=self.lifespan
        )

    def _add_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routes(self):
        self.app.include_router(api_router)

    def create_app(self) -> FastAPI:
        self._add_middlewares()
        self._register_routes()
        return self.app
