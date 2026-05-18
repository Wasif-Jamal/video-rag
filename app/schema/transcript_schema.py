from typing import List, Literal

from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str


class TranscriptResponse(BaseModel):
    video_id: str
    transcript_path: str
    source_type: Literal[
        "captions",
        "whisper",
        "cached",
    ]
    segment_count: int
    segments: List[TranscriptSegment]