from fastapi import APIRouter, HTTPException
from services.ai_service.agents.orchestrator_agent import AgentsOrchestrator
from services.ai_service.modules.logging.models import (TextFoodLogInput, ImageFoodLogInput, InsightsInputs,
                                                        ImageExtraInput)
from services.ai_service.modules.enums import AgentModuleEnum, AgentName
from fastapi import UploadFile, File
import logging
from fastapi import Form
from typing import Optional
import json

logger = logging.getLogger(__name__)

logging_router = APIRouter()
orchestrator = AgentsOrchestrator()

@logging_router.post("/nutrition_text_logging")
async def nutrition_text_logging(
    user_id: Optional[str] = None,
    date: Optional[int] = None,
    body: TextFoodLogInput = None,
):
    try:
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.NUTRITION.value,
            agent=AgentName.NUTRITION_TEXT_LOGGING.value,
            user_id=user_id,
            date=date,
            direct_inputs=body,
        )

        if error:
            logger.error(f"Food logging failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to log food: {error}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in nutrition_text_logging for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@logging_router.post("/nutrition_image_logging")
async def nutrition_image_logging(
        image: UploadFile = File(...),
        body: Optional[str] = Form(None),
        user_id: Optional[str] = Form(None),
        date: Optional[int] = Form(None),
):
    try:
        if body:
            try:
                body_data = json.loads(body)
                extra_input = ImageExtraInput(**body_data)
            except json.JSONDecodeError:
                extra_input = ImageExtraInput(locale=body)
        else:
            extra_input = ImageExtraInput()

        direct_inputs = ImageFoodLogInput(
            image_content=await image.read(),
            extra=extra_input
        )
        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.NUTRITION.value,
            agent=AgentName.NUTRITION_IMAGE_LOGGING.value,
            user_id=user_id,
            date=date,
            direct_inputs=direct_inputs,
        )

        if error:
            logger.error(f"Image food logging failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to log food from image: {error}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in nutrition_image_logging for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@logging_router.post("/nutrition_label_image_logging")
async def nutrition_label_image_logging(
        image: UploadFile = File(...),
        body: Optional[str] = Form(None),
        user_id: Optional[str] = None,
        date: Optional[int] = None,
):
    try:
        if body:
            try:
                body_data = json.loads(body)
                extra_input = ImageExtraInput(**body_data)
            except json.JSONDecodeError:
                extra_input = ImageExtraInput(locale=body)
        else:
            extra_input = ImageExtraInput()

        direct_inputs = ImageFoodLogInput(
            image_content=await image.read(),
            extra=extra_input
        )

        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.NUTRITION.value,
            agent=AgentName.NUTRITION_LABEL_IMAGE_LOGGING.value,
            user_id=user_id,
            date=date,
            direct_inputs=direct_inputs
        )

        if error:
            logger.error(f"Label image logging failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to extract nutrition from label: {error}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in nutrition_label_image_logging for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@logging_router.post("/add_food")
async def add_food(
        body: InsightsInputs,
        user_id: Optional[str] = None,
        date: Optional[int] = None,
):
    try:


        result, error = await orchestrator.run_agents_for_module(
            module=AgentModuleEnum.NUTRITION.value,
            agent=AgentName.NUTRITION_INSIGHTS.value,
            user_id=user_id,
            date=date,
            direct_inputs=body
        )

        if error:
            logger.error(f"Label image logging failed for user {user_id}: {error}")
            raise HTTPException(status_code=400, detail=f"Failed to extract nutrition from label: {error}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in nutrition_label_image_logging for user {user_id}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")