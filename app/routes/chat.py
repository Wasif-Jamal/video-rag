from fastapi import (
    APIRouter,
)

from app.schema.chat_schema import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import (
    chat_service,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    return (
        chat_service.chat(
            session_id=request.session_id,
            query=request.query
        )
    )