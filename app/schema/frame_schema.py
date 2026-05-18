from pydantic import BaseModel


class FrameMetadata(BaseModel):
    timestamp: int
    frame_path: str


class FrameExtractionResponse(BaseModel):
    video_id: str
    frame_count: int
    frames: list[FrameMetadata]