import json
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple

from services.ai_service.base_agent import BaseAgent
from services.ai_service.modules.persona.models import MenstruationPersonaUpdateInput
from services.ai_service.modules.persona.models import MenstruationPersonaUpdateOutput
from services.ai_service.modules.enums import AgentName
from services.ai_service.utils.prompt_builder import PromptBuilder

logger = logging.getLogger("celery")


class MenstruationPersonaAgent(BaseAgent):
    """
    Agent for updating menstruation user persona based on daily logs.
    Synthesizes daily health data into a long-term health narrative.
    """

    @staticmethod
    def _resolve_today(inputs: MenstruationPersonaUpdateInput) -> str:
        """
        Pick the latest `log_date` from the daily log as the authoritative
        "today" anchor for date arithmetic; fall back to UTC today if every
        entry omits it.
        """
        try:
            dates = [
                entry.log_date
                for entry in (inputs.daily_log or [])
                if getattr(entry, "log_date", None)
            ]
            if dates:
                return max(dates)
        except Exception:
            pass
        return datetime.now(timezone.utc).date().isoformat()

    async def run(self, inputs: MenstruationPersonaUpdateInput, cached_content_name: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            today = self._resolve_today(inputs)

            user_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.MENSTRUATION_PERSONA_UPDATE.value,
                data=inputs,
                today=today,
            )

            response, error = self.query_llm(
                prompt=user_prompt,
                output_schema=MenstruationPersonaUpdateOutput,
                cached_content_name=cached_content_name,
            )

            if error:
                logger.error(f"MenstruationPersonaAgent LLM error: {error}")
                return None, error

            return response, None

        except Exception as e:
            logger.exception("MenstruationPersonaAgent failed")
            return None, str(e)
