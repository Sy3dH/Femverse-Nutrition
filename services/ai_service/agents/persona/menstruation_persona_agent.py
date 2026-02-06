import json
import logging
from typing import Optional, Dict, Any, Tuple, Union

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
        inputs: Union[MenstruationPersonaUpdateInput, Dict[str, Any]]
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Update the menstruation persona with today's daily log.

        Args:
            inputs: Either MenstruationPersonaUpdateInput or dict containing
                   'previous_persona' and 'daily_log'

        Returns:
            Tuple of (updated_persona_dict, error_message)
        """
        try:
            # Normalize inputs to plain dicts
            if isinstance(inputs, dict):
                previous_persona = inputs.get("previous_persona", {})
                daily_log = inputs.get("daily_log", {})
            else:
                previous_persona = inputs.previous_persona.model_dump()
                daily_log = inputs.daily_log.model_dump()

            # Build context for PromptBuilder (pre-serialized JSON strings)
            context_data = {
                "previous_persona": json.dumps(previous_persona, indent=2, ensure_ascii=False),
                "daily_log": json.dumps(daily_log, indent=2, ensure_ascii=False),
            }

            # Use PromptBuilder to construct the final prompt
            prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.MENSTRUATION_PERSONA_UPDATE.value,
                data=context_data,
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
