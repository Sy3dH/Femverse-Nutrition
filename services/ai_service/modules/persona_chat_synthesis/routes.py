import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from services.ai_service.modules.persona_chat_synthesis.request_models import (
    ChatPersonaSynthesisRequest,
)
from services.ai_service.modules.persona_chat_synthesis.synthesis_service import (
    synthesize_chat_persona,
)

logger = logging.getLogger(__name__)

chat_persona_router = APIRouter()


@chat_persona_router.post("/chat-persona/synthesize")
async def synthesize_persona_from_chat(
    body: ChatPersonaSynthesisRequest,
    user_id: Optional[str] = None,
):
    """
    Build or update a menstruation (``module`` = ``M``) or pregnancy (``P``) persona from
    dated chat transcripts plus optional stored daily logs / prior persona (when ``user_id`` is wired).
    """
    try:
        result, error = await synthesize_chat_persona(body, user_id)
        if error:
            logger.error("chat-persona synthesize failed user_id=%s: %s", user_id, error)
            raise HTTPException(status_code=400, detail=f"Persona synthesis failed: {error}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in synthesize_persona_from_chat")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
