import json
from pathlib import Path
from typing import List
from app.config.log_config import LogConfig
from app.schema.transcript_schema import TranscriptSegment

logger = LogConfig.get_logger(__name__)

class TranscriptUtils:
    @staticmethod
    def normalize_youtube_captions(captions: List[dict]) -> List[TranscriptSegment]:
        """
        Converts youtube-transcript-api output to TranscriptSegment format.
        """
        normalized = []
        for c in captions:
            start = float(c['start'])
            end = float(start + c['duration'])
            text = c['text'].strip()
            if text:
                normalized.append(TranscriptSegment(start=start, end=end, text=text))
        return normalized

    @staticmethod
    def normalize_whisper_segments(segments: List[dict]) -> List[TranscriptSegment]:
        """
        Converts openai-whisper output to TranscriptSegment format.
        """
        normalized = []
        for s in segments:
            start = float(s['start'])
            end = float(s['end'])
            text = s['text'].strip()
            if text:
                normalized.append(TranscriptSegment(start=start, end=end, text=text))
        return normalized

    @staticmethod
    def save_transcript(video_id: str, segments: List[TranscriptSegment]) -> str:
        """
        Saves the transcript JSON to storage/transcripts/raw/{video_id}.json.
        Returns the absolute path to the saved file.
        """
        target_dir = Path("storage/transcripts/raw")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = target_dir / f"{video_id}.json"
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([seg.model_dump() for seg in segments], f, indent=2, ensure_ascii=False)
            logger.info(f"Transcript saved successfully to {file_path}")
            return str(file_path.absolute())
        except Exception as e:
            logger.error(f"Failed to save transcript for {video_id}: {str(e)}")
            raise e
