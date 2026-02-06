from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from services.ai_service.agents.orchestrator_agent import AgentsOrchestrator
from services.ai_service.modules.persona.models import (
    MenstruationPersonaUpdateInput,
    PregnancyPersonaUpdateInput,
)
from services.ai_service.modules.enums import AgentModuleEnum, AgentName

logger = logging.getLogger(__name__)

persona_router = APIRouter()
orchestrator = AgentsOrchestrator()


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
        direct_inputs = body.model_dump()
        
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
        direct_inputs = body.model_dump()
        
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
