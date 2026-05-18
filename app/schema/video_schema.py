from pydantic import BaseModel

from app.schema.transcript_schema import (
    TranscriptResponse
)

from app.schema.frame_schema import (
    FrameExtractionResponse
)

from app.schema.frame_schema import (
    FrameExtractionResponse,
)


class YouTubeRequest(BaseModel):
    url: str


class VideoMetadata(BaseModel):
    url: str
    video_id: str
    title: str
    duration: int
    channel: str
    local_path: str


class VideoIngestionResponse(BaseModel):
    video: VideoMetadata
    transcript: TranscriptResponse
    frames: FrameExtractionResponse