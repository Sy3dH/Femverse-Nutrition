from fastapi import FastAPI
from services.ai_service.modules.nutrition.routes import nutrition_routes
from services.ai_service.modules.logging.routes import logging_router

app = FastAPI(title="AI Agents API")

app.include_router(nutrition_routes, prefix="/nutrition-ai-service", tags=["Nutrition Plans"])
app.include_router(logging_router, prefix="/logging-ai-service", tags=["Nutrition Logging"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Let's help you with the nutrition 🍇🍈🍉."}