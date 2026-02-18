import logging
from typing import Optional, Dict, Any, Tuple, Union
from services.ai_service.gemini_service import get_gemini_service
from services.ai_service.agents.nutrition.nutrition_agent import NutritionAgent
from services.ai_service.agents.logging.nutrition_insights_agent import NutritionInsightsAgent
from services.ai_service.agents.logging.nutrition_text_logging_agent import NutritionTextLoggingAgent
from services.ai_service.agents.logging.nutrition_image_logging_agent import NutritionImageLoggingAgent
from services.ai_service.agents.logging.nutrition_image_label_logging_agent import NutritionLabelImageLoggingAgent
from services.ai_service.agents.persona.menstruation_persona_agent import MenstruationPersonaAgent
from services.ai_service.agents.persona.pregnancy_persona_agent import PregnancyPersonaAgent
from services.ai_service.modules.enums import AgentName, AgentModuleEnum
from services.ai_service.modules.nutrition.models import NutritionInputs
from services.ai_service.modules.logging.models import (TextFoodLogInput, ImageFoodLogInput, InsightsInputs,
                                                       )
from services.ai_service.modules.persona.models import (MenstruationPersonaUpdateInput, PregnancyPersonaUpdateInput,
                                                       )
from services.ai_service.resolvers.nutrition_resolver import NutritionInputResolver
from services.ai_service.resolvers.nutrition_tip_resolver import NutritionTipInputResolver

logger = logging.getLogger("celery")

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
            },
            AgentModuleEnum.PERSONA.value: {
                AgentName.MENSTRUATION_PERSONA_UPDATE.value: {
                    "agent": MenstruationPersonaAgent(llm_service=llm_service),
                    "resolver": None,  # Direct inputs only
                },
                AgentName.PREGNANCY_PERSONA_UPDATE.value: {
                    "agent": PregnancyPersonaAgent(llm_service=llm_service),
                    "resolver": None,  # Direct inputs only
                },
            }
        }

    async def run_agents_for_module(
            self,
            module: str,
            agent: str,
            user_id: Optional[str] = None,
            date: Optional[int] = None,
            direct_inputs: Optional[Union[NutritionInputs, InsightsInputs,TextFoodLogInput, ImageFoodLogInput, MenstruationPersonaUpdateInput, PregnancyPersonaUpdateInput]] = None,
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