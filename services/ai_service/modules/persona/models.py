from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union, Literal

# Import existing models to reuse for daily logs
from services.ai_service.modules.nutrition.models import (
    MenstrualCycleData,
    TryToConceiveData,
    MenstrualUserLoggedData,
    PregnancyMetaData,
    PregnancyUserLoggedData,
)


# Source attribution for any persona observation that originates from the user.
# - self_reported: stated by the user via chatbot but not yet corroborated
# - clinician_confirmed: user explicitly stated a clinician confirmed it
# - inferred: derived from accumulated daily-log patterns by the LLM
Source = Literal["self_reported", "clinician_confirmed", "inferred"]


# ============== DAILY LOG INPUTS ==============
class LifestyleAndConsumption(BaseModel):
    """
    Tracks daily food, hydration, sleep, and habits.
    """
    breakfast: Optional[str] = None
    lunch: Optional[str] = None
    dinner: Optional[str] = None
    water_intake_liters: Optional[float] = None
    alcohol_units: Optional[int] = None
    caffeine_servings: Optional[int] = None
    smoking_status: Optional[str] = None
    sleephours: Optional[float] = None

class ChatbotInputs(BaseModel):
    """
    Chatbot memories for any additional information provided by the user.
    Defaults to an empty list so downstream prompt rendering never sees a
    literal ``None`` for this field.
    """
    chatbot_memories: List[str] = Field(default_factory=list)

class MenstruationDailyLogInput(BaseModel):
    """
    Daily log input for menstruation tracking.
    Matches POC/Menstruation/Input_Daily_Logs.json structure.
    Reuses existing models from nutrition module.
    """
    log_date: Optional[str] = Field(
        default=None,
        description=(
            "ISO-8601 YYYY-MM-DD date this log entry refers to. "
            "API layer defaults this to today (UTC) when missing so the LLM "
            "always has a temporal anchor for date arithmetic."
        ),
    )
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_ft: Optional[str] = None
    BMI: Optional[float] = None
    cycle_data: Optional[MenstrualCycleData] = None
    try_to_conceive: Optional[TryToConceiveData] = None
    user_logged_data: Optional[MenstrualUserLoggedData] = None
    lifestyle_and_consumption: Optional[LifestyleAndConsumption] = None


class PregnancyDailyLogInput(BaseModel):
    """
    Daily log input for pregnancy tracking.
    Matches POC/Pregnancy/Input_Daily_Logs.json structure.
    Reuses existing models from nutrition module.
    """
    log_date: Optional[str] = Field(
        default=None,
        description=(
            "ISO-8601 YYYY-MM-DD date this log entry refers to. "
            "API layer defaults this to today (UTC) when missing so the LLM "
            "always has a temporal anchor for date arithmetic."
        ),
    )
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_ft: Optional[str] = None
    BMI: Optional[float] = None
    pregnancy_data: Optional[PregnancyMetaData] = None
    user_logged_data: Optional[PregnancyUserLoggedData] = None
    lifestyle_and_consumption: Optional[LifestyleAndConsumption] = None


# ============== PERSONA SUB-STRUCTURES ==============

class IdentityBaseline(BaseModel):
    """Basic identity and health baseline information."""
    age: Optional[int] = None
    baseline_vitals: Optional[str] = None
    general_health_summary: Optional[str] = None


class PhaseSpecificPatterns(BaseModel):
    """Menstrual phase-specific symptom and behavior patterns."""
    menstrual: Optional[str] = None
    follicular: Optional[str] = None
    ovulation: Optional[str] = None
    luteal: Optional[str] = None


class ReproductiveHealth(BaseModel):
    """Reproductive health summary for menstruation persona."""
    cycle_health: Optional[str] = None
    hormonal_sensitivity_profile: Optional[str] = None
    fertility_context: Optional[str] = None
    phase_specific_patterns: Optional[PhaseSpecificPatterns] = None


class TrimesterPatterns(BaseModel):
    """Trimester-specific patterns for pregnancy."""
    first_trimester: Optional[str] = None
    second_trimester: Optional[str] = None
    third_trimester: Optional[str] = None


class PregnancyJourney(BaseModel):
    """Pregnancy journey tracking for pregnancy persona."""
    current_week: Optional[int] = None
    current_trimester: Optional[str] = None
    trimester_specific_patterns: Optional[TrimesterPatterns] = None


class AnomalyBufferItem(BaseModel):
    """Individual anomaly being watched in symptom memory."""
    symptom: str
    first_seen: Optional[str] = None
    occurrences: Optional[int] = None
    context: Optional[str] = None
    status: Optional[str] = None
    pregnancy_week: Optional[int] = None  # For pregnancy-specific tracking
    source: Optional[Source] = None


class SymptomMemory(BaseModel):
    """Long-term memory of symptom patterns and anomalies."""
    chronic_patterns: Optional[str] = None
    symptom_clusters: Optional[str] = None
    body_signals: Optional[str] = None
    anomaly_buffer: Optional[List[AnomalyBufferItem]] = None


class EmotionalProfile(BaseModel):
    """Emotional and psychological patterns."""
    baseline_mood: Optional[str] = None
    stress_physiology: Optional[str] = None
    hormonal_mood_map: Optional[str] = None
    coping_patterns: Optional[str] = None
    mood_patterns: Optional[str] = None  # For pregnancy


class BeneficialIntervention(BaseModel):
    """Lifestyle intervention that has shown positive effects."""
    intervention: str
    observed_effect: Optional[str] = None
    confidence: Optional[str] = None


class DetrimentalTrigger(BaseModel):
    """Lifestyle factor that has shown negative effects."""
    trigger: str
    observed_effect: Optional[str] = None
    confidence: Optional[str] = None


class LifestyleMatrix(BaseModel):
    """Lifestyle patterns and their health correlations."""
    dietary_pattern: Optional[str] = None
    supplement_routine: Optional[str] = None
    prenatal_supplement_routine: Optional[str] = None  # For pregnancy
    physical_activity_baseline: Optional[str] = None
    sleep_pattern: Optional[str] = None  # For pregnancy
    beneficial_interventions: Optional[List[BeneficialIntervention]] = None
    detrimental_triggers: Optional[List[DetrimentalTrigger]] = None


class HealthFlag(BaseModel):
    """Health concern flag with supporting evidence and recommendations."""
    flag_id: str
    signal: Optional[str] = None
    medical_parallel: Optional[str] = None
    supporting_evidence: Optional[List[str]] = None
    confidence: Optional[str] = None
    trend: Optional[str] = None
    urgency: Optional[str] = None  # For pregnancy
    recommendation: Optional[str] = None
    first_flagged: Optional[str] = None
    last_updated: Optional[str] = None
    pregnancy_week_flagged: Optional[int] = None  # For pregnancy
    source: Optional[Source] = None


class HealthWatchlist(BaseModel):
    """Active and resolved health flags with protective factors."""
    active_flags: Optional[List[HealthFlag]] = None
    resolved_flags: Optional[List[HealthFlag]] = None
    protective_factors: Optional[List[str]] = None


class LongitudinalTrends(BaseModel):
    """Long-term health trends over time."""
    cycle_regularity_trend: Optional[str] = None  # For menstruation
    symptom_intensity_trend: Optional[str] = None
    energy_trend: Optional[str] = None
    weight_trend: Optional[str] = None
    mood_trend: Optional[str] = None  # For pregnancy
    sleep_trend: Optional[str] = None  # For pregnancy
    notable_shifts: Optional[str] = None


# ============== COMPLETE PERSONA STRUCTURES ==============

class MenstruationPersona(BaseModel):
    """
    Complete menstruation user persona structure.
    Matches POC/Menstruation/Input_Persona.json schema.
    """
    last_updated: Optional[str] = None
    persona_version: Optional[str] = None
    identity_baseline: Optional[IdentityBaseline] = None
    reproductive_health: Optional[ReproductiveHealth] = None
    symptom_memory: Optional[SymptomMemory] = None
    emotional_profile: Optional[EmotionalProfile] = None
    lifestyle_matrix: Optional[LifestyleMatrix] = None
    health_watchlist: Optional[HealthWatchlist] = None
    longitudinal_trends: Optional[LongitudinalTrends] = None
    clinician_summary: Optional[str] = None


class PregnancyPersona(BaseModel):
    """
    Complete pregnancy user persona structure.
    Matches POC/Pregnancy/Input_Persona.json schema.
    """
    last_updated: Optional[str] = None
    persona_version: Optional[str] = None
    identity_baseline: Optional[IdentityBaseline] = None
    pregnancy_journey: Optional[PregnancyJourney] = None
    symptom_memory: Optional[SymptomMemory] = None
    emotional_profile: Optional[EmotionalProfile] = None
    lifestyle_matrix: Optional[LifestyleMatrix] = None
    health_watchlist: Optional[HealthWatchlist] = None
    longitudinal_trends: Optional[LongitudinalTrends] = None
    clinician_summary: Optional[str] = None


# ============== API INPUT MODELS ==============

class MenstruationPersonaUpdateInput(BaseModel):
    """
    API input for menstruation persona update endpoint.
    Contains both the previous persona and today's daily log.
    """
    previous_persona: MenstruationPersona
    daily_log: List[MenstruationDailyLogInput]
    chatbot_inputs: Optional[ChatbotInputs] = None


class MenstruationPersonaUpdateOutput(BaseModel):
    """
    API input for menstruation persona update endpoint.
    Contains both the previous persona and today's daily log.
    """
    current_persona: MenstruationPersona


class PregnancyPersonaUpdateInput(BaseModel):
    """
    API input for pregnancy persona update endpoint.
    Contains both the previous persona and today's daily log.
    """
    previous_persona: PregnancyPersona
    daily_log: List[PregnancyDailyLogInput]
    chatbot_inputs: Optional[ChatbotInputs] = None

class PregnancyPersonaUpdateOutput(BaseModel):
    """
    API input for pregnancy persona update endpoint.
    Contains both the previous persona and today's daily log.
    """
    current_persona: PregnancyPersona


# ============== NUTRITION PERSONA ==============

class DigestiveSymptoms(BaseModel):
    """Daily digestive / GI symptom log."""
    bloating: Optional[bool] = None
    constipation: Optional[bool] = None
    acid_reflux: Optional[bool] = None
    nausea: Optional[bool] = None
    other_symptoms: Optional[List[str]] = None


class NutritionDailyLogInput(BaseModel):
    """
    Daily log input for nutrition tracking.
    No menstruation or pregnancy data — standalone nutrition + lifestyle signals.
    """
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_ft: Optional[str] = None
    BMI: Optional[float] = None
    breakfast: Optional[str] = None
    lunch: Optional[str] = None
    dinner: Optional[str] = None
    snacks: Optional[str] = None
    water_intake_liters: Optional[float] = None
    energy_level: Optional[str] = None
    hunger_satiety_pattern: Optional[str] = None
    digestive_symptoms: Optional[DigestiveSymptoms] = None
    mood: Optional[str] = None
    sleep_hours: Optional[float] = None
    physical_activity: Optional[str] = None
    supplements: Optional[List[str]] = None
    alcohol_units: Optional[int] = None
    caffeine_servings: Optional[int] = None
    smoking_status: Optional[str] = None


class NutritionalProfile(BaseModel):
    """Observed dietary and nutritional patterns over time."""
    dietary_pattern_summary: Optional[str] = None
    macro_balance_observation: Optional[str] = None
    micronutrient_gaps_suspected: Optional[str] = None
    hydration_pattern: Optional[str] = None
    meal_timing_behavior: Optional[str] = None
    food_sensitivities_observed: Optional[str] = None
    dietary_restrictions: Optional[str] = None


class DigestiveHealth(BaseModel):
    """Long-term digestive and gut health patterns."""
    gi_pattern_summary: Optional[str] = None
    food_symptom_correlations: Optional[str] = None
    bloating_trigger_pattern: Optional[str] = None
    gut_health_signals: Optional[str] = None


class NutritionLongitudinalTrends(BaseModel):
    """Long-term nutrition and health trends over time."""
    dietary_consistency_trend: Optional[str] = None
    digestive_health_trend: Optional[str] = None
    energy_trend: Optional[str] = None
    weight_trend: Optional[str] = None
    mood_trend: Optional[str] = None
    notable_shifts: Optional[str] = None


class NutritionPersona(BaseModel):
    """
    Complete nutrition user persona structure.
    Tracks dietary patterns, digestive health, and nutrition-related
    lifestyle signals independently of menstruation or pregnancy data.
    """
    last_updated: Optional[str] = None
    persona_version: Optional[str] = None
    identity_baseline: Optional[IdentityBaseline] = None
    nutritional_profile: Optional[NutritionalProfile] = None
    digestive_health: Optional[DigestiveHealth] = None
    symptom_memory: Optional[SymptomMemory] = None
    emotional_profile: Optional[EmotionalProfile] = None
    lifestyle_matrix: Optional[LifestyleMatrix] = None
    health_watchlist: Optional[HealthWatchlist] = None
    longitudinal_trends: Optional[NutritionLongitudinalTrends] = None
    clinician_summary: Optional[str] = None


class NutritionPersonaUpdateInput(BaseModel):
    """
    API input for nutrition persona update endpoint.
    Contains the previous persona, today's daily log(s), and optional chatbot inputs.
    """
    previous_persona: NutritionPersona
    daily_log: List[NutritionDailyLogInput]
    chatbot_inputs: Optional[ChatbotInputs] = None


class NutritionPersonaUpdateOutput(BaseModel):
    """
    API output for nutrition persona update endpoint.
    """
    current_persona: NutritionPersona


# ============== FITNESS PERSONA ==============

class WorkoutLog(BaseModel):
    """Single workout session details."""
    activity_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    intensity: Optional[str] = None
    perceived_exertion: Optional[str] = None
    workout_notes: Optional[str] = None


class FitnessDailyLogInput(BaseModel):
    """
    Daily log input for fitness tracking.
    Captures workout, recovery, sleep, and lifestyle signals.
    No menstruation or pregnancy data.
    """
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_ft: Optional[str] = None
    BMI: Optional[float] = None
    workout_log: Optional[WorkoutLog] = None
    rest_day: Optional[bool] = None
    muscle_soreness: Optional[str] = None
    energy_level: Optional[str] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[str] = None
    water_intake_liters: Optional[float] = None
    nutrition_snapshot: Optional[str] = None
    mood: Optional[str] = None
    stress_level: Optional[str] = None
    injury_notes: Optional[str] = None
    supplements: Optional[List[str]] = None
    steps_count: Optional[int] = None


class FitnessProfile(BaseModel):
    """Long-term fitness capability and training pattern summary."""
    current_fitness_level: Optional[str] = None
    primary_fitness_goal: Optional[str] = None
    preferred_activities: Optional[str] = None
    training_frequency_pattern: Optional[str] = None
    workout_consistency: Optional[str] = None
    strength_endurance_observations: Optional[str] = None


class RecoveryProfile(BaseModel):
    """Long-term recovery and rest pattern summary."""
    sleep_pattern_summary: Optional[str] = None
    typical_recovery_time: Optional[str] = None
    overtraining_signals: Optional[str] = None
    injury_history: Optional[str] = None
    fatigue_patterns: Optional[str] = None


class FitnessLongitudinalTrends(BaseModel):
    """Long-term fitness and body composition trends over time."""
    fitness_progression_trend: Optional[str] = None
    workout_consistency_trend: Optional[str] = None
    recovery_trend: Optional[str] = None
    energy_trend: Optional[str] = None
    weight_trend: Optional[str] = None
    mood_trend: Optional[str] = None
    notable_shifts: Optional[str] = None


class FitnessPersona(BaseModel):
    """
    Complete fitness user persona structure.
    Tracks training patterns, recovery, body composition, and
    performance-related lifestyle signals independently of
    menstruation or pregnancy data.
    """
    last_updated: Optional[str] = None
    persona_version: Optional[str] = None
    identity_baseline: Optional[IdentityBaseline] = None
    fitness_profile: Optional[FitnessProfile] = None
    recovery_profile: Optional[RecoveryProfile] = None
    symptom_memory: Optional[SymptomMemory] = None
    emotional_profile: Optional[EmotionalProfile] = None
    lifestyle_matrix: Optional[LifestyleMatrix] = None
    health_watchlist: Optional[HealthWatchlist] = None
    longitudinal_trends: Optional[FitnessLongitudinalTrends] = None
    clinician_summary: Optional[str] = None


class FitnessPersonaUpdateInput(BaseModel):
    """
    API input for fitness persona update endpoint.
    Contains the previous persona, today's daily log(s), and optional chatbot inputs.
    """
    previous_persona: FitnessPersona
    daily_log: List[FitnessDailyLogInput]
    chatbot_inputs: Optional[ChatbotInputs] = None


class FitnessPersonaUpdateOutput(BaseModel):
    """
    API output for fitness persona update endpoint.
    """
    current_persona: FitnessPersona
