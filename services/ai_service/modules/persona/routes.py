from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from services.ai_service.agents.orchestrator_agent import AgentsOrchestrator
from services.ai_service.modules.persona.models import (
    MenstruationPersonaUpdateInput,
    PregnancyPersonaUpdateInput,
    NutritionPersonaUpdateInput,
    FitnessPersonaUpdateInput,
)
from services.ai_service.modules.enums import AgentModuleEnum, AgentName

logger = logging.getLogger(__name__)

persona_router = APIRouter()
orchestrator = AgentsOrchestrator()


def _default_log_dates(daily_log) -> None:
    """
    Ensure every daily-log entry carries an ISO-8601 ``log_date``. Any entry
    that omits it (or sends ``None``) is defaulted to today (UTC) so the
    persona-update prompt always receives a temporal anchor for date math.
    """
    today_iso = datetime.now(timezone.utc).date().isoformat()
    if not daily_log:
        return
    for entry in daily_log:
        if getattr(entry, "log_date", None):
            continue
        try:
            entry.log_date = today_iso
        except Exception:
            pass


@persona_router.post("/menstruation/update")
async def update_menstruation_persona(
    body: MenstruationPersonaUpdateInput,
    user_id: Optional[str] = None,
):
    """
    Update a menstruation user persona based on daily log data.
    
    This endpoint synthesizes daily health data into a long-term health narrative,
    tracking patterns, correlations, and health flags over time.
    
    Args:
        body: Contains previous_persona and daily_log
        user_id: Optional user identifier for logging purposes
    
    Returns:
        Updated persona JSON with synthesized health patterns
    """
    try:
        _default_log_dates(body.daily_log)
        direct_inputs = body
        
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=AgentName.MENSTRUATION_PERSONA_UPDATE.value,
            user_id=user_id,
            direct_inputs=direct_inputs,
        )

        if error:
            logger.error(f"Menstruation persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")
        
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in update_menstruation_persona for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@persona_router.post("/pregnancy/update")
async def update_pregnancy_persona(
    body: PregnancyPersonaUpdateInput,
    user_id: Optional[str] = None,
):
    """
    Update a pregnancy user persona based on daily log data.
    
    This endpoint synthesizes daily pregnancy health data into a long-term health narrative,
    tracking patterns, symptoms, and health flags throughout the pregnancy journey.
    
    Args:
        body: Contains previous_persona and daily_log
        user_id: Optional user identifier for logging purposes
    
    Returns:
        Updated persona JSON with synthesized pregnancy health patterns
    """
    try:
        _default_log_dates(body.daily_log)
        direct_inputs = body
        
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=AgentName.PREGNANCY_PERSONA_UPDATE.value,
            user_id=user_id,
            direct_inputs=direct_inputs,
        )

        if error:
            logger.error(f"Pregnancy persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")
        
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in update_pregnancy_persona for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@persona_router.post("/nutrition/update")
async def update_nutrition_persona(
    body: NutritionPersonaUpdateInput,
    user_id: Optional[str] = None,
):
    """
    Update a nutrition user persona based on daily log data.

    This endpoint synthesizes daily meal, hydration, digestive, and lifestyle
    data into a long-term nutritional health narrative, tracking dietary patterns,
    food-symptom correlations, and nutrition-related health flags over time.

    Args:
        body: Contains previous_persona and daily_log
        user_id: Optional user identifier for logging purposes

    Returns:
        Updated persona JSON with synthesized nutritional patterns
    """
    try:
        direct_inputs = body

        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=AgentName.NUTRITION_PERSONA_UPDATE.value,
            user_id=user_id,
            direct_inputs=direct_inputs,
        )

        if error:
            logger.error(f"Nutrition persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in update_nutrition_persona for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@persona_router.post("/fitness/update")
async def update_fitness_persona(
    body: FitnessPersonaUpdateInput,
    user_id: Optional[str] = None,
):
    """
    Update a fitness user persona based on daily log data.

    This endpoint synthesizes daily workout, recovery, sleep, and lifestyle
    data into a long-term fitness health narrative, tracking training patterns,
    recovery baselines, and fitness-related health flags over time.

    Args:
        body: Contains previous_persona and daily_log
        user_id: Optional user identifier for logging purposes

    Returns:
        Updated persona JSON with synthesized fitness patterns
    """
    try:
        direct_inputs = body

        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=AgentName.FITNESS_PERSONA_UPDATE.value,
            user_id=user_id,
            direct_inputs=direct_inputs,
        )

        if error:
            logger.error(f"Fitness persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in update_fitness_persona for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")