import json
import logging
from typing import Optional, Dict, Any, Tuple

from services.ai_service.base_agent import BaseAgent
from services.ai_service.modules.persona.models import PregnancyPersonaUpdateInput
from services.ai_service.modules.persona.models import PregnancyPersonaUpdateOutput
from services.ai_service.modules.enums import AgentName
from services.ai_service.utils.prompt_builder import PromptBuilder

logger = logging.getLogger("celery")


class PregnancyPersonaAgent(BaseAgent):
    """
    Agent for updating pregnancy user persona based on daily logs.
    Synthesizes daily pregnancy health data into a long-term health narrative.
    """

    async def run(self, inputs: PregnancyPersonaUpdateInput, cached_content_name: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Update the pregnancy persona with today's daily log.

        Args:
            inputs: PregnancyPersonaUpdateInput containing
                   'previous_persona' and 'daily_log'

        Returns:
            Tuple of (updated_persona_dict, error_message)
        """
        try:

            # Use PromptBuilder to construct the final prompt
            user_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.PREGNANCY_PERSONA_UPDATE.value,
                data=inputs,
            )

            # Call LLM using default temperature and no explicit system prompt
            response, error = self.query_llm(
                prompt=user_prompt,
                cached_content_name=cached_content_name,
                output_schema=PregnancyPersonaUpdateOutput,
            )

            if error:
                logger.error(f"PregnancyPersonaAgent LLM error: {error}")
                return None, error

            return response, None

        except Exception as e:
            logger.exception("PregnancyPersonaAgent failed")
            return None, str(e)
