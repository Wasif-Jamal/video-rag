from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class EnvConfig(BaseSettings):
    """
    Environment configuration
    for Video RAG system.
    """

    # API Keys
    GOOGLE_API_KEY: str

    # Storage Paths
    STORAGE_DIR: str = "storage"

    VIDEO_DIR: str = (
        "storage/videos"
    )

    TRANSCRIPT_DIR: str = (
        "storage/transcripts/raw"
    )

    FRAME_DIR: str = (
        "storage/frames"
    )

    # Qdrant
    QDRANT_URL: str = (
        "http://localhost:6333"
    )

    COLLECTION_NAME: str = (
        "video_rag_multimodal"
    )

    # Models
    CLIP_MODEL_NAME: str = (
        "openai/clip-vit-base-patch32"
    )

    GEMINI_MODEL_NAME: str = (
        "models/gemma-4-26b-a4b-it"
    )

    # Video Constraints
    MAX_VIDEO_DURATION: int = 420

    FRAME_EXTRACTION_INTERVAL: int = 2

    model_config = (
        SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
        )
    )


@lru_cache
def get_config() -> EnvConfig:
    """
    Returns cached config instance.
    """

    return EnvConfig()


config = get_config()