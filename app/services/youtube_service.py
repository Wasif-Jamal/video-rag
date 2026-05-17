import yt_dlp
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    def get_metadata(self, url: str) -> dict:
        """
        Extracts metadata from a YouTube URL without downloading the video.
        """
        ydl_opts = {
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'channel': info.get('channel') or info.get('uploader'),
                }
        except Exception as e:
            logger.error(f"Failed to fetch metadata for {url}: {str(e)}")
            raise e

youtube_service = YouTubeService()
