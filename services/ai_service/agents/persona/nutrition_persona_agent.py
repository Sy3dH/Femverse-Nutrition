import logging
from typing import Optional, Dict, Any, Tuple

from services.ai_service.base_agent import BaseAgent
from services.ai_service.modules.persona.models import (
    NutritionPersonaUpdateInput,
    NutritionPersonaUpdateOutput,
)
from services.ai_service.modules.enums import AgentName
from services.ai_service.utils.prompt_builder import PromptBuilder

logger = logging.getLogger("celery")


class NutritionPersonaAgent(BaseAgent):
    """
    Agent for updating the nutrition user persona based on daily logs.
    Synthesizes meal, hydration, digestive, and lifestyle data into a
    long-term nutritional health narrative.
    """

    async def run(
        self,
        inputs: NutritionPersonaUpdateInput,
        cached_content_name: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            user_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.NUTRITION_PERSONA_UPDATE.value,
                data=inputs,
            )

            response, error = self.query_llm(
                prompt=user_prompt,
                output_schema=NutritionPersonaUpdateOutput,
                cached_content_name=cached_content_name,
            )

            if error:
                logger.error(f"NutritionPersonaAgent LLM error: {error}")
                return None, error

            return response, None

        except Exception as e:
            logger.exception("NutritionPersonaAgent failed")
            return None, str(e)
