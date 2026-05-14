from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field


class ChatTurn(BaseModel):
    role: str
    content: str


class ChatSession(BaseModel):
    date: str
    chat_transcript: List[ChatTurn] = Field(default_factory=list)


class ChatPersonaSynthesisRequest(BaseModel):
    """
    Request body aligned with persona sample JSON:
    ``module`` ``M`` = menstruation, ``P`` = pregnancy; ``chats`` holds dated transcripts.
    """

    module: Literal["M", "P"]
    chats: List[ChatSession] = Field(default_factory=list)
