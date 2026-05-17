import subprocess
import whisper
from pathlib import Path
from typing import List
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)

class WhisperService:
    def __init__(self):
        self.model = None

    def _get_model(self):
        if self.model is None:
            logger.info("Loading Whisper 'base' model...")
            self.model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully.")
        return self.model

    def _extract_audio(self, video_path: str, video_id: str) -> str:
        """
        Extracts audio from video using FFmpeg and saves it to storage/audio/.
        Returns the path to the extracted audio file.
        """
        audio_dir = Path("storage/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        audio_path = audio_dir / f"{video_id}.mp3"
        
        if audio_path.exists():
            logger.info(f"Audio already extracted at {audio_path}")
            return str(audio_path)

        logger.info(f"Extracting audio from {video_path} to {audio_path} using FFmpeg")
        
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",          
            "-acodec", "libmp3lame",
            "-q:a", "2",    
            "-y",           
            str(audio_path)
        ]
        
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Audio extraction successful for {video_id}")
            return str(audio_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg audio extraction failed for {video_id}: {e.stderr.decode()}")
            raise Exception("Failed to extract audio from video.") from e

    def transcribe(self, video_path: str, video_id: str) -> List[dict]:
        """
        Extracts audio and runs Whisper transcription.
        Returns the raw Whisper segments.
        """
        audio_path = self._extract_audio(video_path, video_id)
        
        model = self._get_model()
        logger.info(f"Starting Whisper transcription for {video_id} using {audio_path}")
        
        result = model.transcribe(audio_path)
        
        logger.info(f"Whisper transcription completed for {video_id}")
        return result.get("segments", [])

whisper_service = WhisperService()
