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
from services.ai_service.agents.persona.nutrition_persona_agent import NutritionPersonaAgent
from services.ai_service.agents.persona.fitness_persona_agent import FitnessPersonaAgent
from services.ai_service.modules.enums import AgentName, AgentModuleEnum
from services.ai_service.modules.nutrition.models import NutritionInputs
from services.ai_service.modules.logging.models import (TextFoodLogInput, ImageFoodLogInput, InsightsInputs,
                                                       )
from services.ai_service.resolvers.nutrition_resolver import NutritionInputResolver
from services.ai_service.utils.system_prompts import AGENT_SYSTEM_PROMPTS
from services.ai_service.modules.persona.models import (
    MenstruationPersonaUpdateInput,
    PregnancyPersonaUpdateInput,
    NutritionPersonaUpdateInput,
    FitnessPersonaUpdateInput,
)

logger = logging.getLogger("celery")

class AgentsOrchestrator:
    def __init__(self):
        self.llm_service = get_gemini_service()
        self.registry = {
            AgentModuleEnum.NUTRITION.value: {
                AgentName.NUTRITION.value: {
                    "agent": NutritionAgent(llm_service=self.llm_service),
                    "resolver": NutritionInputResolver(),
                },
                AgentName.NUTRITION_INSIGHTS.value: {
                    "agent": NutritionInsightsAgent(llm_service=self.llm_service),
                    "resolver": None,
                },
                AgentName.NUTRITION_TEXT_LOGGING.value: {
                    "agent": NutritionTextLoggingAgent(llm_service=self.llm_service),
                    "resolver": None,
                },
                AgentName.NUTRITION_IMAGE_LOGGING.value: {
                    "agent": NutritionImageLoggingAgent(llm_service=self.llm_service),
                    "resolver": None,
                },
                AgentName.NUTRITION_LABEL_IMAGE_LOGGING.value: {
                    "agent": NutritionLabelImageLoggingAgent(llm_service=self.llm_service),
                    "resolver": None,
                }
            },
            AgentModuleEnum.PERSONA.value: {},
        }

        # Each persona module has TWO agent-name variants (single-log and
        # batch-log) that share a single agent instance. The orchestrator
        # registers BOTH variants against the SAME shared instance so the
        # route layer can dispatch either mode without us having to keep
        # two duplicate object graphs in memory.
        menstruation_agent = MenstruationPersonaAgent(llm_service=self.llm_service)
        pregnancy_agent = PregnancyPersonaAgent(llm_service=self.llm_service)
        nutrition_persona_agent = NutritionPersonaAgent(llm_service=self.llm_service)
        fitness_agent = FitnessPersonaAgent(llm_service=self.llm_service)

        persona_registry = self.registry[AgentModuleEnum.PERSONA.value]
        for agent_name_enum, agent_instance in (
            (AgentName.MENSTRUATION_PERSONA_UPDATE_SINGLE, menstruation_agent),
            (AgentName.MENSTRUATION_PERSONA_UPDATE_BATCH, menstruation_agent),
            (AgentName.PREGNANCY_PERSONA_UPDATE_SINGLE, pregnancy_agent),
            (AgentName.PREGNANCY_PERSONA_UPDATE_BATCH, pregnancy_agent),
            (AgentName.NUTRITION_PERSONA_UPDATE_SINGLE, nutrition_persona_agent),
            (AgentName.NUTRITION_PERSONA_UPDATE_BATCH, nutrition_persona_agent),
            (AgentName.FITNESS_PERSONA_UPDATE_SINGLE, fitness_agent),
            (AgentName.FITNESS_PERSONA_UPDATE_BATCH, fitness_agent),
        ):
            persona_registry[agent_name_enum.value] = {
                "agent": agent_instance,
                "resolver": None,  # Direct inputs only
            }

    def _resolve_cache_name(self, agent_name: str) -> Optional[str]:

        system_prompt = AGENT_SYSTEM_PROMPTS.get(agent_name)

        if not system_prompt:
            logger.debug(f"[Orchestrator] Agent '{agent_name}' has no SYSTEM_PROMPT — skipping cache.")
            return None

        cache_name = self.llm_service.cache_registry.get_or_create(
            display_name=agent_name,
            system_instruction=system_prompt,
        )

        print("Currently created caches", self.llm_service.cache_registry.list_cached())
        if not cache_name:
           logger.warning(
                f"[Orchestrator] Cache unavailable for '{agent_name}' — proceeding without cache."
            )

        return cache_name

    async def run_agents_for_module(
            self,
            module: str,
            agent: str,
            user_id: Optional[str] = None,
            date: Optional[int] = None,
            direct_inputs: Optional[Union[NutritionInputs, InsightsInputs, TextFoodLogInput, ImageFoodLogInput, MenstruationPersonaUpdateInput, PregnancyPersonaUpdateInput, NutritionPersonaUpdateInput, FitnessPersonaUpdateInput]] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:

        if module not in self.registry:
            return None, f"Module {module} not configured"

        if agent not in self.registry[module]:
            return None, f"Agent {agent} not configured for module {module}"


        agent_entry = self.registry[module][agent]
        agent_instance = agent_entry["agent"]

        resolver = agent_entry.get("resolver")
        cached_content_name = self._resolve_cache_name(agent)

        print(cached_content_name)

        if direct_inputs:
            logger.info(f"Running {agent} with direct inputs")
            # Persona agents accept an `agent_name` kwarg so the SINGLE-vs-BATCH
            # variant is propagated to the prompt builder. Non-persona agents
            # ignore the kwarg via **kwargs; we send it unconditionally only to
            # persona agents (which we detect by module).
            if module == AgentModuleEnum.PERSONA.value:
                result, error = await agent_instance.run(
                    direct_inputs,
                    cached_content_name=cached_content_name,
                    agent_name=agent,
                )
            else:
                result, error = await agent_instance.run(direct_inputs, cached_content_name)
        else:
            if not user_id:
                return None, "user_id required when direct_inputs not provided"
            if not resolver:
                return None, f"No resolver configured for agent {agent}"

            logger.info(f"Resolving inputs for {agent} module={module} user_id={user_id}")
            inputs = await resolver.resolve(user_id=user_id, date=date)
            result, error = await agent_instance.run(cached_content_name=cached_content_name, **inputs)

        if error:
            return result, error

        return result, error