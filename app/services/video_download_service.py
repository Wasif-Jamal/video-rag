import yt_dlp
from pathlib import Path
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)

class VideoDownloadService:
    def __init__(self):
        self.download_dir = Path("storage/videos")
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download_video(self, url: str, video_id: str) -> str:
        """
        Downloads a video to storage/videos/{video_id}.mp4.
        Returns the absolute local path.
        """
        local_path = self.download_dir / f"{video_id}.mp4"
        
        if local_path.exists():
            logger.info(f"Video {video_id} already exists at {local_path}")
            return str(local_path.absolute())

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(self.download_dir / '%(id)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Downloading video {video_id}...")
                ydl.download([url])
                return str(local_path.absolute())
        except Exception as e:
            logger.error(f"Failed to download video {url}: {str(e)}")
            raise e

video_download_service = VideoDownloadService()
