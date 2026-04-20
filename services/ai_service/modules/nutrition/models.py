from pydantic import BaseModel, Field
from typing import Optional, Dict, Any,Literal, Union, List

MealLabel = Literal[
    "Brunch",
    "Breakfast",
    "Morning Snack",
    "Lunch",
    "Snack",
    "Evening Snack",
    "Dinner"
]


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

class MenstrualCycleData(BaseModel):
    average_cycle_length: Optional[int] = None
    previous_cycle_lengths: Optional[List[int]] = None
    current_cycle_type: Optional[str] = None
    current_cycle_day: Optional[int] = None
    current_cycle_phase: Optional[str] = None
    current_phase_day: Optional[int] = None
    late_period_flag: Optional[str] = None


class TryToConceiveData(BaseModel):
    trying_to_conceive: Optional[bool] = None
    sexual_activities: Optional[List[str]] = None
    sexual_feelings: Optional[str] = None
    ovulation_test: Optional[str] = None


class MenstrualUserLoggedData(BaseModel):
    symptoms: Optional[List[str]] = None
    gastrointestinal: Optional[List[str]] = None
    blood_flow_level: Optional[str] = None
    vaginal_discharges: Optional[List[str]] = None
    moods: Optional[List[str]] = None
    sleep_quality: Optional[str] = None
    diet_type: Optional[str] = None
    supplements: Optional[List[str]] = None
    other_activities: Optional[List[str]] = None
    physical_activities: Optional[List[str]] = None


class MenstrualDataInput(BaseModel):
    cycle_data: Optional[MenstrualCycleData] = None
    try_to_conceive: Optional[TryToConceiveData] = None
    user_logged_data: Optional[MenstrualUserLoggedData] = None

class PregnancyMetaData(BaseModel):
    pregnancy_week: Optional[int] = None
    trimester: Optional[str] = None


class PregnancyUserLoggedData(BaseModel):
    daily_feelings: Optional[List[str]] = None
    breast_symptoms: Optional[List[str]] = None
    swelling_symptoms: Optional[List[str]] = None
    gastrointestinal_symptoms: Optional[List[str]] = None
    mood_symptoms: Optional[List[str]] = None
    general_symptoms: Optional[List[str]] = None
    vaginal_discharges: Optional[List[str]] = None
    sleep_quality: Optional[str] = None
    physical_activity: Optional[str] = None
    supplements: Optional[List[str]] = None


class PregnancyDataInput(BaseModel):
    pregnancy_data: Optional[PregnancyMetaData] = None
    user_logged_data: Optional[PregnancyUserLoggedData] = None

class NutritionInputs(BaseModel):
    onboarding_data: Optional[OnboardingNutritionInput] = None
    menstrual_data: Optional[MenstrualDataInput] = None
    pregnancy_data: Optional[PregnancyDataInput] = None
    bmi: Optional[float] = None
    bmr: Optional[float] = None
    country: Optional[str] = None
    food_prefs: Optional[str] = None
    medical_condition: Optional[List[str]] = None
    cuisine: Optional[str] = None
    allergies: Optional[str] = None
    target_calories: Optional[int] = None
    health_goals: Optional[str] = None
    current_weight: Optional[str] = None
    weight_change_rate: Optional[str] = None
    target_weight: Optional[float] = None
    activity_level: Optional[str] = None
    meals_per_day: Optional[int] = Field(default=3, ge=2, le=5)
    alerts: List[str] = []
    menstruation_persona: Optional[Dict[str, Any]] = None
    pregnancy_persona: Optional[Dict[str, Any]] = None
    language: Optional[str] = None
    timezone: Optional[str] = None


class NutritionInputsDummy(BaseModel):
    onboarding_data: Optional[OnboardingNutritionInput] = None # We want this
    menstrual_data: Optional[MenstrualDataInput] = None
    pregnancy_data: Optional[PregnancyDataInput] = None
    menstruation_persona: Optional[Dict[str, Any]] = None
    pregnancy_persona: Optional[Dict[str, Any]] = None


class Ingredient(BaseModel):
    item: str
    quantity: str

class Recipe(BaseModel):
    ingredients: List[Ingredient]
    instructions: List[str]

class Nutrition(BaseModel):
    calories: float
    protein_g: float
    carbs_g: float
    fats_g: float

class Meal(BaseModel):
    meal_label: MealLabel
    name: str
    recipe: Recipe
    target_calories: int
    nutrition: Nutrition

class Meals(BaseModel):
    meal_1: Meal
    meal_2: Meal
    meal_3: Optional[Meal] = None
    meal_4: Optional[Meal] = None
    meal_5: Optional[Meal] = None

class DailyPlan(BaseModel):
    day: int
    focus: str
    daily_calorie_target: int
    meals: Meals

class ThreeDayPlan(BaseModel):
    plan_type: str
    plan_template: str
    cycle_phase_or_trimester: Optional[str] = None
    three_day_plan: List[DailyPlan]
    reasoning: str
