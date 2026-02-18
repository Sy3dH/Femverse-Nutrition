from typing import Optional, Dict, Any, Tuple
import logging
from services.ai_service.base_agent import BaseAgent
from services.ai_service.utils.prompt_builder import PromptBuilder
from services.ai_service.modules.enums import AgentName
from services.ai_service.modules.logging.models import TextFoodLogInput, TextFoodLogOutput

logger = logging.getLogger("celery")

class NutritionTextLoggingAgent(BaseAgent):

    async def run(
            self,
            inputs: TextFoodLogInput,
            cached_content_name: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            nutrition_user_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.NUTRITION_TEXT_LOGGING.value,
                data=inputs
            )

            response, error = self.query_llm(
                prompt=nutrition_user_prompt,
                output_schema=TextFoodLogOutput,
                cached_content_name=cached_content_name,
            )

            if error:
                return None, error

            return response, None

        except Exception as e:
            logger.exception("NutritionTextLoggingAgent failed")
            return None, str(e)