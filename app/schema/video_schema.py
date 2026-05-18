from pydantic import BaseModel

from app.schema.transcript_schema import (
    TranscriptResponse,
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