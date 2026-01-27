from typing import Optional, Dict, Any, Tuple
import logging
from services.ai_service.base_agent import BaseAgent
from services.ai_service.utils.prompt_builder import PromptBuilder
from services.ai_service.modules.enums import AgentName
from services.ai_service.modules.logging.models import TextFoodLogInput, TextFoodLogOutput

logger = logging.getLogger("celery")

class NutritionTextLoggingAgent(BaseAgent):
    async def run(self, inputs: TextFoodLogInput) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            nutrition_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.NUTRITION_TEXT_LOGGING.value,
                data=inputs
            )

            response, error = self.query_llm(
                prompt=nutrition_prompt,
                output_schema=TextFoodLogOutput,
            )

            if error:
                return None, error

            return response, None

        except Exception as e:
            logger.exception("NutritionAgent failed")
            return None, str(e)

