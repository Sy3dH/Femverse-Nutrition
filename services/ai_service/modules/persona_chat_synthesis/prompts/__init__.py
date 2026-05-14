"""Domain-specific system prompts for chat → persona synthesis."""

from services.ai_service.modules.persona_chat_synthesis.prompts.extract_facts_menstruation import (
    EXTRACT_FACTS_SYSTEM_MENSTRUATION,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.extract_facts_pregnancy import (
    EXTRACT_FACTS_SYSTEM_PREGNANCY,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.merge_persona_menstruation import (
    MERGE_CHAT_INTO_PERSONA_SYSTEM_MENSTRUATION,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.merge_persona_pregnancy import (
    MERGE_CHAT_INTO_PERSONA_SYSTEM_PREGNANCY,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.new_persona_menstruation import (
    NEW_PERSONA_FROM_CHAT_SYSTEM_MENSTRUATION,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.new_persona_pregnancy import (
    NEW_PERSONA_FROM_CHAT_SYSTEM_PREGNANCY,
)

__all__ = [
    "EXTRACT_FACTS_SYSTEM_MENSTRUATION",
    "EXTRACT_FACTS_SYSTEM_PREGNANCY",
    "MERGE_CHAT_INTO_PERSONA_SYSTEM_MENSTRUATION",
    "MERGE_CHAT_INTO_PERSONA_SYSTEM_PREGNANCY",
    "NEW_PERSONA_FROM_CHAT_SYSTEM_MENSTRUATION",
    "NEW_PERSONA_FROM_CHAT_SYSTEM_PREGNANCY",
]
