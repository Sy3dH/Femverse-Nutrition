from typing import Optional, Dict, Any, Tuple
import logging
from services.ai_service.base_agent import BaseAgent
from services.ai_service.utils.prompt_builder import PromptBuilder
from services.ai_service.modules.enums import AgentName
from services.ai_service.modules.logging.models import ImageFoodLogInput, ImageFoodLogOutput

logger = logging.getLogger("celery")

class NutritionImageLoggingAgent(BaseAgent):
    async def run(
        self,
        inputs: ImageFoodLogInput
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            logging_prompt = PromptBuilder.build_prompt(
                agent_name=AgentName.NUTRITION_IMAGE_LOGGING.value,
                data=inputs.extra
            )

            response, error = self.query_llm(
                prompt=logging_prompt,
                image_bytes=inputs.image_content,
                output_schema=ImageFoodLogOutput
            )

            if error:
                return None, error

            return response, None

        except Exception as e:
            logger.exception("NutritionImageLoggingAgent failed")
            return None, str(e)

