import logging
from typing import Optional, Dict, Any, Tuple, Union
from services.ai_service.gemini_service import get_gemini_service
from services.ai_service.agents.nutrition.nutrition_agent import NutritionAgent
from services.ai_service.agents.logging.nutrition_insights_agent import NutritionInsightsAgent
from services.ai_service.agents.logging.nutrition_text_logging_agent import NutritionTextLoggingAgent
from services.ai_service.agents.logging.nutrition_image_logging_agent import NutritionImageLoggingAgent
from services.ai_service.agents.logging.nutrition_image_label_logging_agent import NutritionLabelImageLoggingAgent
from services.ai_service.modules.enums import AgentName, AgentModuleEnum
from services.ai_service.modules.nutrition.models import NutritionInputs
from services.ai_service.modules.logging.models import (TextFoodLogInput, ImageFoodLogInput, InsightsInputs,
                                                       )
from services.ai_service.resolvers.nutrition_resolver import NutritionInputResolver
from services.ai_service.resolvers.nutrition_tip_resolver import NutritionTipInputResolver
from pathlib import Path
import json

logger = logging.getLogger("celery")
IMAGE_LOGGING_JSON = Path("D:\\9DTechWork\\FemVerse-Nutrition\\services\\Tests\\data\\nutrition_insights_image_menustral_data.json")
NUTRITION_LOGGING_JSON = Path("D:\\9DTechWork\\FemVerse-Nutrition\\services\\Tests\\data\\nutrition_insights_labels_menustral_data.json")

class AgentsOrchestrator:
    def __init__(self):
        llm_service = get_gemini_service()
        self.registry = {
            AgentModuleEnum.NUTRITION.value: {
                AgentName.NUTRITION.value: {
                    "agent": NutritionAgent(llm_service=llm_service),
                    "resolver": NutritionInputResolver(),
                },
                AgentName.NUTRITION_INSIGHTS.value: {
                    "agent": NutritionInsightsAgent(llm_service=llm_service),
                    "resolver": NutritionInputResolver(),
                },
                AgentName.NUTRITION_TEXT_LOGGING.value: {
                    "agent": NutritionTextLoggingAgent(llm_service=llm_service),
                    "resolver": NutritionTipInputResolver(),
                },
                AgentName.NUTRITION_IMAGE_LOGGING.value: {
                    "agent": NutritionImageLoggingAgent(llm_service=llm_service),
                    "resolver": NutritionTipInputResolver(),
                },
                AgentName.NUTRITION_LABEL_IMAGE_LOGGING.value: {
                    "agent": NutritionLabelImageLoggingAgent(llm_service=llm_service),
                    "resolver": NutritionTipInputResolver(),
                }
            }
        }

    async def run_agents_for_module(
            self,
            module: str,
            agent: str,
            user_id: Optional[str] = None,
            date: Optional[int] = None,
            direct_inputs: Optional[Union[NutritionInputs, InsightsInputs,TextFoodLogInput, ImageFoodLogInput]] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:

        if module not in self.registry:
            return None, f"Module {module} not configured"

        if agent not in self.registry[module]:
            return None, f"Agent {agent} not configured for module {module}"

        agent_entry = self.registry[module][agent]
        agent_instance = agent_entry["agent"]
        resolver = agent_entry.get("resolver")

        if direct_inputs:
            logger.info(f"Running {agent} with direct inputs")
            result, error = await agent_instance.run(direct_inputs)
        else:
            if not user_id:
                return None, "user_id required when direct_inputs not provided"
            if not resolver:
                return None, f"No resolver configured for agent {agent}"

            logger.info(f"Resolving inputs for {agent} module={module} user_id={user_id}")
            inputs = await resolver.resolve(user_id=user_id, date=date)
            result, error = await agent_instance.run(**inputs)

        if error:
            return result, error

        return result, error

    # async def _generate_insights_from_text_logging(
    #         self,
    #         result: Dict[str, Any],
    #         user_id: Optional[str],
    #         date: Optional[int],
    #         original_inputs: Optional[InsightsTextInputs]
    # ) -> Dict[str, Any]:
    #
    #     if not result:
    #         return {"food_nutrients": None, "insights": None}
    #
    #     original_inputs.current_nutrients = result
    #
    #     insights, insight_error = await self.run_agents_for_module(
    #         module=AgentModuleEnum.NUTRITION.value,
    #         agent=AgentName.NUTRITION_INSIGHTS.value,
    #         user_id=user_id,
    #         date=date,
    #         direct_inputs=original_inputs
    #     )
    #
    #     return {
    #         "food_nutrients": result,
    #         "insights": insights,
    #         "insights_error": insight_error
    #     }
    #
    # async def _generate_insights_from_image_logging(
    #         self,
    #         result: Dict[str, Any],
    #         user_id: Optional[str],
    #         date: Optional[int],
    #         original_inputs: Optional[ImageFoodLogInput]
    # ) -> Dict[str, Any]:
    #     """Post-processor for image logging to generate insights"""
    #
    #     if not result or not result.get("foods"):
    #         return {"foods": [], "total_nutrients": None, "insights": None}
    #
    #     # Calculate total nutrients
    #     total_nutrients = {
    #         "calories": sum(food.get("calories", 0) for food in result["foods"]),
    #         "carbs": sum(food.get("carbs", 0) for food in result["foods"]),
    #         "protein": sum(food.get("protein", 0) for food in result["foods"]),
    #         "fats": sum(food.get("fats", 0) for food in result["foods"])
    #     }
    #
    #     food_names = ", ".join(food.get("name", "Unknown") for food in result["foods"])
    #
    #     # Load dummy data for insights context
    #     try:
    #         with IMAGE_LOGGING_JSON.open("r", encoding='utf-8') as file:
    #             all_dummy_cases = json.load(file)
    #         dummy_body = InsightsImageInputs(**all_dummy_cases[0]) if all_dummy_cases else None
    #     except Exception as e:
    #         logger.warning(f"Failed to load dummy insights data: {e}")
    #         dummy_body = InsightsImageInputs()
    #
    #     if dummy_body:
    #         dummy_body.log_input.food_name = food_names
    #         dummy_body.current_nutrients = total_nutrients
    #
    #     # Call insights agent
    #     insights, insight_error = await self.run_agents_for_module(
    #         module=AgentModuleEnum.NUTRITION.value,
    #         agent=AgentName.NUTRITION_INSIGHTS.value,
    #         user_id=user_id,
    #         date=date,
    #         direct_inputs=dummy_body
    #     )
    #
    #     return {
    #         "foods": result["foods"],
    #         "total_nutrients": total_nutrients,
    #         "insights": insights,
    #         "insights_error": insight_error
    #     }
    #
    # async def _generate_insights_from_label_logging(
    #         self,
    #         result: Dict[str, Any],
    #         user_id: Optional[str],
    #         date: Optional[int],
    #         original_inputs: Optional[ImageFoodLogInput]
    # ) -> Dict[str, Any]:
    #     """Post-processor for nutrition label logging to generate insights"""
    #
    #     if not result:
    #         return {"food_nutrients": None, "insights": None}
    #
    #     try:
    #         with NUTRITION_LOGGING_JSON.open("r", encoding='utf-8') as file:
    #             all_dummy_cases = json.load(file)
    #         dummy_body = InsightsImageInputs(**all_dummy_cases[0]) if all_dummy_cases else None
    #     except Exception as e:
    #         logger.warning(f"Failed to load dummy insights data: {e}")
    #         dummy_body = InsightsImageInputs()
    #
    #     if dummy_body:
    #         dummy_body.log_input.food_name = result.get("food_name", "Unknown")
    #         dummy_body.current_nutrients = {
    #             "calories": result.get("calories", 0),
    #             "fats": result.get("fats", 0),
    #             "protein": result.get("protein", 0),
    #             "carbs": result.get("carbs", 0)
    #         }
    #
    #     current_nutrients = dummy_body.current_nutrients if dummy_body else {}
    #
    #     insights, insight_error = await self.run_agents_for_module(
    #         module=AgentModuleEnum.NUTRITION.value,
    #         agent=AgentName.NUTRITION_INSIGHTS.value,
    #         user_id=user_id,
    #         date=date,
    #         direct_inputs=dummy_body
    #     )
    #
    #     return {
    #         "food_nutrients": current_nutrients,
    #         "insights": insights,
    #         "insights_error": insight_error
    #     }