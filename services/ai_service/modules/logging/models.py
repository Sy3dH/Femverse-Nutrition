from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field

class ImageExtraInput(BaseModel):
    lang: str
    timezone: str

class ImageFoodLogInput(BaseModel):
    image_content: bytes
    extra: Optional[ImageExtraInput]

class NutritionFoodItem(BaseModel):
    package_name: str
    calories: float
    carbs: float
    protein: float
    fats: float

class FoodItem(BaseModel):
    name: str
    calories: float
    carbs: float
    protein: float
    fats: float

class TextFoodItem(BaseModel):
    name: str
    servings: float
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
    lang: str
    timezone: str

class OnboardingResponseItem(BaseModel):
    question_code: str
    answer: Union[str, int, List[str]]

class OnboardingNutritionInput(BaseModel):
    responses: List[OnboardingResponseItem] = Field(
        ..., description="List of onboarding question responses"
    )
    more_about_user: Optional[str] = Field(
        None, description="Free text about the user"
    )
    get_pregnant: Optional[bool] = Field(
        False, description="Whether the user has a goal to get pregnant"
    )

class InsightsInputs(BaseModel):
    persona: Optional[Dict[str, Any]] = None # TODO: @hanzalah5 needs to verify this
    onboarding_data: Optional[OnboardingNutritionInput] = None
    log_input: Optional[TextFoodLogInput] = None
    current_nutrients: Optional[Dict[str, Any]] = None
    target_weight: Optional[float] = None
    current_weight: Optional[float] = None
    weight_change_rate: Optional[float] = None
    meal_plan: Optional[Dict[str, Any]] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

class TextFoodLogOutput(BaseModel):
    status: int
    foods: List[TextFoodItem]
    error: Optional[str] = None
    verbose_reasoning: str

class NutritionFoodLogOutput(BaseModel):
    status: int
    foods: List[NutritionFoodItem]
    error: Optional[str] = None
    verbose_reasoning: str

class NutritionTip(BaseModel):
    title: str
    body: str

class Alerts(BaseModel):
    title: str
    body: str

class InsightLogOutput(BaseModel):
    nutrition_tip: List[NutritionTip]
    insights: str
    is_alert_to_change_meal_plan: bool
    alerts: List[Alerts]
