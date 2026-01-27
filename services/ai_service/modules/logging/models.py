import base64
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, field_validator

class ImageFoodLogInput(BaseModel):
    image_content: bytes

class FoodItem(BaseModel):
    name: str
    calories: float
    carbs: float
    protein: float
    fats: float

class ImageFoodLogOutput(BaseModel):
    foods: List[FoodItem]


class TextFoodLogInput(BaseModel):
    food_name: str

class InsightsInputs(BaseModel):
    log_input: TextFoodLogInput
    target_weight: Optional[float] = None
    current_weight: Optional[float] = None
    loosing_weight_rate: Optional[float] = None
    health_analysis: Optional[str] = None
    meal_plan: Optional[Dict[str, Any]] = None
    current_nutrients: Optional[Dict[str, Any]] = None

class TextFoodLogOutput(BaseModel):
    calories: float
    carbs: float
    protein: float
    fats: float

class NutritionFoodLogOutput(BaseModel):
    food_name: str
    calories: float
    carbs: float
    protein: float
    fats: float

class InsightLogOutput(BaseModel):
    nutrition_tip: str
    insights: str
    is_alert_to_change_meal_plan: bool
    alerts: List[str]
