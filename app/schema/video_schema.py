from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    url: str

class DownloadedVideoResponse(BaseModel):
    url: str
    video_id: str
    title: str
    duration: int
    channel: str
    local_path: str
