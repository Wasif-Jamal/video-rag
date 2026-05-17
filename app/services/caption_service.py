from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from app.config.log_config import LogConfig
from typing import List, Optional

logger = LogConfig.get_logger(__name__)

class CaptionService:
    def get_captions(self, video_id: str) -> Optional[List[dict]]:
        """
        Fetches English captions for a YouTube video if available.
        Returns None if not found or disabled.
        """
        try:
            logger.info(f"Attempting to fetch captions for video: {video_id}")
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id, languages=['en'])
            logger.info(f"Successfully fetched captions for video: {video_id}")
            return [
                {'text': snippet.text, 'start': snippet.start, 'duration': snippet.duration}
                for snippet in transcript
            ]
        except (TranscriptsDisabled, NoTranscriptFound):
            logger.info(f"No English captions found for video: {video_id}")
            return None
        except Exception as e:
            logger.warning(f"Failed to fetch captions for video {video_id}: {str(e)}")
            return None

caption_service = CaptionService()
