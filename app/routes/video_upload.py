from fastapi import APIRouter, HTTPException, status
from app.schema.video_schema import YouTubeRequest, DownloadedVideoResponse
from app.utils.youtube_validators import validate_youtube_url
from app.services.youtube_service import youtube_service
from app.services.video_download_service import video_download_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/video", tags=["Video Upload"])

@router.post("/youtube", response_model=DownloadedVideoResponse)
async def upload_youtube_video(request: YouTubeRequest):
    url = request.url
    
    # 1. Validate URL
    if not validate_youtube_url(url):
        logger.warning(f"Invalid YouTube URL provided: {url}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL. Please provide a valid youtube.com or youtu.be URL."
        )
    
    try:
        # 2. Fetch metadata
        logger.info(f"Fetching metadata for {url}")
        metadata = youtube_service.get_metadata(url)
        
        duration = metadata.get("duration")
        if not duration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not retrieve video duration."
            )
            
        # 3. Reject if duration > 420 seconds (7 minutes)
        if duration > 420:
            logger.warning(f"Video rejected: duration {duration}s > 420s")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Video is too long ({duration}s). Maximum allowed length is 6 minutes (360s)."
            )
            
        # 4. Download video
        video_id = metadata["id"]
        logger.info(f"Starting download for video ID: {video_id}")
        local_path = video_download_service.download_video(url, video_id)
        
        # 5. Return response schema
        return DownloadedVideoResponse(
            url=url,
            video_id=video_id,
            title=metadata["title"],
            duration=duration,
            channel=metadata.get("channel", "Unknown"),
            local_path=local_path
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing YouTube video: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the video."
        )
