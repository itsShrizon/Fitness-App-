from fastapi import APIRouter, HTTPException, Depends
from app.schemas.models import ChatRequest
from app.services.chat_service import chat_service, ChatService

router = APIRouter()

@router.post("/chat", response_model=str)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(lambda: chat_service)
):
    try:
        return await service.get_response(
            message=request.message,
            chat_history=request.history,
            context=request.context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
