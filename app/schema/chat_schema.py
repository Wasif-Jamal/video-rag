from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class RetrievedImage(BaseModel):
    image_path: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    images: list[RetrievedImage]