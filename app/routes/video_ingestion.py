from fastapi import APIRouter, HTTPException, status

from app.schema.video_schema import (
    YouTubeRequest,
    VideoIngestionResponse,
)
from app.services.video_ingestion_service import (
    video_ingestion_service,
)
from app.utils.youtube_validators import (
    validate_youtube_url,
)
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)

router = APIRouter(
    prefix="/video",
    tags=["Video Ingestion"],
)


@router.post(
    "/youtube",
    response_model=VideoIngestionResponse,
)
async def ingest_youtube_video(
    request: YouTubeRequest,
):

    url = str(request.url)

    # 1. Validate URL
    if not validate_youtube_url(url):
        logger.warning(
            f"Invalid YouTube URL provided: {url}"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid YouTube URL. "
                "Please provide a valid "
                "youtube.com or youtu.be URL."
            ),
        )

    try:

        logger.info(
            f"Starting ingestion pipeline for: {url}"
        )

        result = (
            await video_ingestion_service
            .ingest_youtube_video(url)
        )

        return result

    except HTTPException:
        raise

    except ValueError as exc:

        logger.warning(str(exc))

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:

        logger.exception(
            f"Video ingestion failed: {str(exc)}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An error occurred while "
                "processing the video."
            ),
        )