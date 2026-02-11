from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class ImageFoodLogInput(BaseModel):
    image_content: bytes

class FoodItem(BaseModel):
    name: str
    calories: float
    carbs: float
    protein: float
    fats: float

class ImageFoodLogOutput(BaseModel):
    status: int
    foods: List[FoodItem]
    error: Optional[str] = None
    verbose_reasoning: str

class TextFoodLogInput(BaseModel):
    food_name: str
    locale:str

class InsightsInputs(BaseModel):
    log_input: TextFoodLogInput
    current_nutrients: Optional[Dict[str, Any]] = None
    target_weight: Optional[float] = None
    current_weight: Optional[float] = None
    weight_change_rate: Optional[float] = None
    health_analysis: Optional[str] = None
    meal_plan: Optional[Dict[str, Any]] = None

class TextFoodLogOutput(BaseModel):
    status: int
    foods: List[FoodItem]
    error: Optional[str] = None
    verbose_reasoning: str

class NutritionFoodLogOutput(BaseModel):
    status: int
    foods: List[FoodItem]
    error: Optional[str] = None
    verbose_reasoning: str

class InsightLogOutput(BaseModel):
    nutrition_tip: str
    insights: str
    is_alert_to_change_meal_plan: bool
    alerts: List[str]
