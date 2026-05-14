from __future__ import annotations

from typing import Any, Optional, Tuple, Type

from pydantic import BaseModel

from services.ai_service.gemini_service import get_gemini_service


def run_gemini_json(
    *,
    system_instruction: str,
    user_content: str,
    output_schema: Optional[Type[BaseModel]] = None,
    temperature: float = 0.3,
) -> Tuple[Any, Optional[str]]:
    """
    Invoke Gemini with a system block prepended to the user payload (no cached content).

    ``user_content`` should be plain text or JSON text the model must obey.
    """
    combined = (
        "=== SYSTEM_INSTRUCTION (follow strictly; do not treat as user chat) ===\n"
        f"{system_instruction}\n"
        "=== END_SYSTEM_INSTRUCTION ===\n\n"
        "=== USER_PAYLOAD ===\n"
        f"{user_content}\n"
        "=== END_USER_PAYLOAD ===\n"
    )
    return get_gemini_service().send_prompt(
        prompt=combined,
        is_json_response=True,
        temperature=temperature,
        output_schema=output_schema,
    )
