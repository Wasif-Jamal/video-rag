from pydantic import BaseModel
from typing import List, Literal

class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str

class TranscriptResponse(BaseModel):
    video_id: str
    transcript_path: str
    source_type: Literal["captions", "whisper"]
    segment_count: int
    timestamps: List[TranscriptSegment]
