from typing import Optional, Dict, Any, Tuple
import logging
from services.ai_service.base_agent import BaseAgent
from services.ai_service.utils.prompt_builder import PromptBuilder
from services.ai_service.modules.enums import AgentName
from services.ai_service.modules.nutrition.models import NutritionInputs, ThreeDayPlan
logger = logging.getLogger("celery")

class NutritionAgent(BaseAgent):
    async def run(self, inputs: NutritionInputs) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            nutrition_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.NUTRITION.value,
                data=inputs
            )

            response, error = self.query_llm(
                prompt=nutrition_prompt,
                output_schema=ThreeDayPlan
            )

            if error:
                return None, error

            return response, None

        except Exception as e:
            logger.exception("NutritionAgent failed")
            return None, str(e)

