from fastapi import APIRouter, HTTPException
from typing import Optional
from services.ai_service.agents.orchestrator_agent import AgentsOrchestrator
from services.ai_service.modules.nutrition.models import NutritionInputs
from services.ai_service.modules.enums import AgentModuleEnum, AgentName, PlanType
from services.ai_service.utils.nutrition_plans import PLAN_TEMPLATES

nutrition_routes = APIRouter()
orchestrator = AgentsOrchestrator()

@nutrition_routes.post("/nutrition_plan")
async def nutrition_plan(
    plan_type: PlanType,
    user_id: Optional[str] = None,
    date: Optional[int] = None,
    body: NutritionInputs = None,
):
    direct_inputs = body.model_dump() if body else None
    direct_inputs["plan_type"] = plan_type.value
    direct_inputs["plan_template"] = PLAN_TEMPLATES[plan_type.value]
    result, error = await orchestrator.run_agents_for_module(
        module=AgentModuleEnum.NUTRITION.value,
        agent=AgentName.NUTRITION.value,
        user_id=user_id,
        date=date,
        direct_inputs=direct_inputs,
    )

    if error:
        raise HTTPException(status_code=400, detail=error)
    return result