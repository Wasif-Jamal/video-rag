from fastapi import HTTPException, status
import json
from app.config.log_config import LogConfig
from app.services.caption_service import caption_service
from app.services.whisper_service import whisper_service
from app.utils.transcript_utils import TranscriptUtils
from app.schema.transcript_schema import TranscriptResponse
from pathlib import Path

logger = LogConfig.get_logger(__name__)

class TranscriptionService:
    def process_transcript(self, video_id: str, local_video_path: str) -> TranscriptResponse:
        """
        Orchestrates the transcription pipeline: Captions -> Whisper Fallback -> Persistence.
        """
        segments = []
        source_type = None

        #1. Check if transcript file already exists
        transcript_path = (
            Path("storage/transcripts/raw")
            / f"{video_id}.json"
        )

        if transcript_path.exists():

            logger.info(
                "Transcript already exists. "
                "Skipping regeneration."
            )

            with open(
                transcript_path,
                "r",
                encoding="utf-8",
            ) as file:

                segments = json.load(file)

            return TranscriptResponse(
                video_id=video_id,
                transcript_path=str(
                    transcript_path
                ),
                source_type="cached",
                segment_count=len(
                    segments
                ),
                segments=segments,
            )
        
        # 2. Try Captions
        logger.info(f"Starting transcription pipeline for {video_id}")
        raw_captions = caption_service.get_captions(video_id)
        
        if raw_captions:
            logger.info(f"Using YouTube captions for {video_id}")
            segments = TranscriptUtils.normalize_youtube_captions(raw_captions)
            source_type = "captions"
        else:
            # 3. Fallback to Whisper
            logger.info(f"Falling back to Whisper for {video_id}")
            if not Path(local_video_path).exists():
                logger.error(f"Video file not found for Whisper fallback: {local_video_path}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Video file not found for transcription."
                )
            
            try:
                raw_segments = whisper_service.transcribe(local_video_path, video_id)
                segments = TranscriptUtils.normalize_whisper_segments(raw_segments)
                source_type = "whisper"
            except Exception as e:
                logger.error(f"Transcription pipeline failed completely for {video_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Transcription failed."
                )
                
        if not segments:
            logger.error(f"No transcript segments could be generated for {video_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Generated transcript was empty."
            )

        # 4. Persist Transcript
        logger.info(f"Persisting transcript for {video_id}")
        transcript_path = TranscriptUtils.save_transcript(video_id, segments)
        
        # 5. Return Metadata
        return TranscriptResponse(
            video_id=video_id,
            transcript_path=transcript_path,
            source_type=source_type,
            segment_count=len(segments),
            segments=segments
        )

transcription_service = TranscriptionService()
