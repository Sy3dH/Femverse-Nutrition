import json
import logging
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

    async def run(
        self,
        inputs: MenstruationPersonaUpdateInput,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.MENSTRUATION_PERSONA_UPDATE.value,
                data=inputs,
            )

            response, error = self.query_llm(
                prompt=prompt,
                output_schema=MenstruationPersonaUpdateOutput,
            )

            if error:
                logger.error(f"MenstruationPersonaAgent LLM error: {error}")
                return None, error

            return response, None

        except Exception as e:
            logger.exception("MenstruationPersonaAgent failed")
            return None, str(e)
