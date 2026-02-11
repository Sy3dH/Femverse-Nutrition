from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union

# Import existing models to reuse for daily logs
from services.ai_service.modules.nutrition.models import (
    MenstrualCycleData,
    TryToConceiveData,
    MenstrualUserLoggedData,
    PregnancyMetaData,
    PregnancyUserLoggedData,
)


# ============== DAILY LOG INPUTS ==============

class MenstruationDailyLogInput(BaseModel):
    """
    Daily log input for menstruation tracking.
    Matches POC/Menstruation/Input_Daily_Logs.json structure.
    Reuses existing models from nutrition module.
    """
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_ft: Optional[str] = None
    BMI: Optional[float] = None
    cycle_data: Optional[MenstrualCycleData] = None
    try_to_conceive: Optional[TryToConceiveData] = None
    user_logged_data: Optional[MenstrualUserLoggedData] = None


class PregnancyDailyLogInput(BaseModel):
    """
    Daily log input for pregnancy tracking.
    Matches POC/Pregnancy/Input_Daily_Logs.json structure.
    Reuses existing models from nutrition module.
    """
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_ft: Optional[str] = None
    BMI: Optional[float] = None
    pregnancy_data: Optional[PregnancyMetaData] = None
    user_logged_data: Optional[PregnancyUserLoggedData] = None


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
    user_id: Optional[str] = None
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
    user_id: Optional[str] = None
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
    daily_log: MenstruationDailyLogInput


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
    daily_log: PregnancyDailyLogInput

class PregnancyPersonaUpdateOutput(BaseModel):
    """
    API input for pregnancy persona update endpoint.
    Contains both the previous persona and today's daily log.
    """
    current_persona: PregnancyPersona
