from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SessionDatedFacts(BaseModel):
    """Facts anchored to one chat session date (YYYY-MM-DD)."""

    session_date: Optional[str] = None
    facts: List[str] = Field(
        default_factory=list,
        description="Atomic, user-grounded facts from that session only.",
    )


class MenstruationChatFactsExtraction(BaseModel):
    """Structured extraction output for menstruation persona synthesis."""

    dated_sessions: List[SessionDatedFacts] = Field(default_factory=list)
    verbatim_self_reported_clinical: List[str] = Field(
        default_factory=list,
        description="Verbatim user-stated diagnoses, meds, allergies, procedures.",
    )
    identity_signals: Optional[str] = None
    reproductive_cycle_signals: Optional[str] = None
    symptom_signals: Optional[str] = None
    emotional_stress_signals: Optional[str] = None
    lifestyle_signals: Optional[str] = None
    discarded_small_talk_summary: Optional[str] = Field(
        default=None,
        description="Brief note of non-health content ignored.",
    )


class PregnancyChatFactsExtraction(BaseModel):
    """Structured extraction output for pregnancy persona synthesis."""

    dated_sessions: List[SessionDatedFacts] = Field(default_factory=list)
    verbatim_self_reported_clinical: List[str] = Field(
        default_factory=list,
        description="Verbatim user-stated GA/weeks, meds, supplements, OB instructions.",
    )
    identity_signals: Optional[str] = None
    pregnancy_journey_signals: Optional[str] = None
    symptom_signals: Optional[str] = None
    emotional_stress_signals: Optional[str] = None
    lifestyle_signals: Optional[str] = None
    discarded_small_talk_summary: Optional[str] = Field(
        default=None,
        description="Brief note of non-health content ignored.",
    )
