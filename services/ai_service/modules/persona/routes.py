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


def _today_iso() -> str:
    """ISO-8601 wall-clock date in UTC; the persona pipeline's single source of truth for `today`."""
    return datetime.now(timezone.utc).date().isoformat()


def _default_log_dates(daily_log) -> None:
    """
    Ensure every daily-log entry carries an ISO-8601 ``log_date``. Any entry
    that omits it (or sends ``None``) is defaulted to today (UTC) so the
    persona-update prompt always receives a temporal anchor for date math.
    """
    if not daily_log:
        return
    today_iso = _today_iso()
    for entry in daily_log:
        if getattr(entry, "log_date", None):
            continue
        try:
            entry.log_date = today_iso
        except Exception:
            pass


def _should_short_circuit(body) -> bool:
    """
    True when there is nothing for the LLM to do: no daily log entries and no
    chatbot memories. We still bump ``last_updated`` to today so the caller
    sees a fresh timestamp, but we skip the LLM call entirely.
    """
    no_logs = not getattr(body, "daily_log", None)
    chatbot_inputs = getattr(body, "chatbot_inputs", None)
    no_memories = (
        chatbot_inputs is None
        or not getattr(chatbot_inputs, "chatbot_memories", None)
    )
    return no_logs and no_memories


def _no_op_response(body, today_iso: str) -> dict:
    """
    Return the previous persona unchanged except for ``last_updated`` bumped
    to today. Used by the no-op short-circuit so the response shape is
    identical to a real agent run.
    """
    prev_dump = body.previous_persona.model_dump()
    prev_dump["last_updated"] = today_iso
    return {"current_persona": prev_dump}


def _enforce_last_updated(result, today_iso: str) -> object:
    """
    Belt-and-suspenders: regardless of what the LLM wrote into
    ``current_persona.last_updated``, stamp the route's wall-clock today
    after a successful agent run. Operates on the orchestrator's dict result
    in place; non-dict results are returned untouched.
    """
    if isinstance(result, dict):
        persona = result.get("current_persona")
        if isinstance(persona, dict):
            persona["last_updated"] = today_iso
    return result


# Mode-dispatch table: (module-prefix) -> (SINGLE-log AgentName, BATCH-log AgentName).
# Kept here at module scope so the dispatch is data-driven and the four routes
# stay structurally identical.
_PERSONA_AGENT_NAME_BY_MODE = {
    "menstruation": (
        AgentName.MENSTRUATION_PERSONA_UPDATE_SINGLE,
        AgentName.MENSTRUATION_PERSONA_UPDATE_BATCH,
    ),
    "pregnancy": (
        AgentName.PREGNANCY_PERSONA_UPDATE_SINGLE,
        AgentName.PREGNANCY_PERSONA_UPDATE_BATCH,
    ),
    "nutrition": (
        AgentName.NUTRITION_PERSONA_UPDATE_SINGLE,
        AgentName.NUTRITION_PERSONA_UPDATE_BATCH,
    ),
    "fitness": (
        AgentName.FITNESS_PERSONA_UPDATE_SINGLE,
        AgentName.FITNESS_PERSONA_UPDATE_BATCH,
    ),
}


def _pick_persona_agent_name(module_key: str, daily_log) -> str:
    """
    Select the SINGLE-LOG or BATCH-LOG persona agent-name variant for the
    given module based on the shape of ``daily_log``.

    Exactly one entry → SINGLE_LOG. Multiple entries → BATCH_LOG. Empty or
    missing daily log → SINGLE_LOG (the route would short-circuit before
    reaching this anyway, but we still need a valid value to log).

    The two variants share an agent class but bind DIFFERENT cached system
    prompts inside Gemini, so this choice determines which prompt the LLM
    actually executes against.
    """
    single, batch = _PERSONA_AGENT_NAME_BY_MODE[module_key]
    if daily_log and len(daily_log) > 1:
        return batch.value
    return single.value


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
        today_iso = _today_iso()
        _default_log_dates(body.daily_log)

        if _should_short_circuit(body):
            logger.info(f"Menstruation persona update short-circuited (no inputs) for user {user_id}")
            return _no_op_response(body, today_iso)

        agent_name = _pick_persona_agent_name("menstruation", body.daily_log)
        logger.info(f"Menstruation persona update dispatching agent={agent_name} for user {user_id}")
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=agent_name,
            user_id=user_id,
            direct_inputs=body,
        )

        if error:
            logger.error(f"Menstruation persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")

        return _enforce_last_updated(result, today_iso)

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
        today_iso = _today_iso()
        _default_log_dates(body.daily_log)

        if _should_short_circuit(body):
            logger.info(f"Pregnancy persona update short-circuited (no inputs) for user {user_id}")
            return _no_op_response(body, today_iso)

        agent_name = _pick_persona_agent_name("pregnancy", body.daily_log)
        logger.info(f"Pregnancy persona update dispatching agent={agent_name} for user {user_id}")
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=agent_name,
            user_id=user_id,
            direct_inputs=body,
        )

        if error:
            logger.error(f"Pregnancy persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")

        return _enforce_last_updated(result, today_iso)

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
        today_iso = _today_iso()
        _default_log_dates(body.daily_log)

        if _should_short_circuit(body):
            logger.info(f"Nutrition persona update short-circuited (no inputs) for user {user_id}")
            return _no_op_response(body, today_iso)

        agent_name = _pick_persona_agent_name("nutrition", body.daily_log)
        logger.info(f"Nutrition persona update dispatching agent={agent_name} for user {user_id}")
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=agent_name,
            user_id=user_id,
            direct_inputs=body,
        )

        if error:
            logger.error(f"Nutrition persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")

        return _enforce_last_updated(result, today_iso)

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
        today_iso = _today_iso()
        _default_log_dates(body.daily_log)

        if _should_short_circuit(body):
            logger.info(f"Fitness persona update short-circuited (no inputs) for user {user_id}")
            return _no_op_response(body, today_iso)

        agent_name = _pick_persona_agent_name("fitness", body.daily_log)
        logger.info(f"Fitness persona update dispatching agent={agent_name} for user {user_id}")
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.PERSONA.value,
            agent=agent_name,
            user_id=user_id,
            direct_inputs=body,
        )

        if error:
            logger.error(f"Fitness persona update failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to update persona: {error}")

        return _enforce_last_updated(result, today_iso)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in update_fitness_persona for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")