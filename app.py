from fastapi import FastAPI
from services.ai_service.modules.nutrition.routes import nutrition_routes
from services.ai_service.modules.logging.routes import logging_router
from services.ai_service.modules.persona.routes import persona_router

app = FastAPI(title="AI Agents API")

app.include_router(nutrition_routes, prefix="/nutrition-ai-service", tags=["Nutrition Plans"])
app.include_router(logging_router, prefix="/logging-ai-service", tags=["Nutrition Logging"])
app.include_router(persona_router, prefix="/persona-ai-service", tags=["Persona Update"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Let's help you with the nutrition 🍇🍈🍉."}