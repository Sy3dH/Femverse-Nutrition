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
            response, error = self.query_llm(
                prompt=PromptBuilder.build_template(AgentName.NUTRITION_IMAGE_LOGGING.value),
                image_bytes=inputs.image_content,
                output_schema=ImageFoodLogOutput
            )

            if error:
                return None, error

            return response, None

        except Exception as e:
            logger.exception("NutritionImageLoggingAgent failed")
            return None, str(e)

