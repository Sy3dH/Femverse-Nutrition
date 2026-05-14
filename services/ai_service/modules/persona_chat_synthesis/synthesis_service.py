from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from services.ai_service.modules.persona.models import (
    MenstruationDailyLogInput,
    MenstruationPersona,
    MenstruationPersonaUpdateOutput,
    PregnancyDailyLogInput,
    PregnancyPersona,
    PregnancyPersonaUpdateOutput,
)
from services.ai_service.modules.persona_chat_synthesis.facts_models import (
    MenstruationChatFactsExtraction,
    PregnancyChatFactsExtraction,
)
from services.ai_service.modules.persona_chat_synthesis.llm_service import run_gemini_json
from services.ai_service.modules.persona_chat_synthesis.persona_data_access import (
    check_existing_persona,
    get_daily_logs,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.extract_facts_menstruation import (
    EXTRACT_FACTS_SYSTEM_MENSTRUATION,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.extract_facts_pregnancy import (
    EXTRACT_FACTS_SYSTEM_PREGNANCY,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.merge_persona_menstruation import (
    MERGE_CHAT_INTO_PERSONA_SYSTEM_MENSTRUATION,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.merge_persona_pregnancy import (
    MERGE_CHAT_INTO_PERSONA_SYSTEM_PREGNANCY,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.new_persona_menstruation import (
    NEW_PERSONA_FROM_CHAT_SYSTEM_MENSTRUATION,
)
from services.ai_service.modules.persona_chat_synthesis.prompts.new_persona_pregnancy import (
    NEW_PERSONA_FROM_CHAT_SYSTEM_PREGNANCY,
)
from services.ai_service.modules.persona_chat_synthesis.request_models import (
    ChatPersonaSynthesisRequest,
)

ModuleCode = Literal["M", "P"]


def resolve_today_from_request(payload: ChatPersonaSynthesisRequest) -> str:
    """Latest chat session date if valid ISO dates exist; else UTC calendar date."""
    dates: List[str] = []
    for session in payload.chats or []:
        d = (session.date or "").strip()
        if len(d) >= 10:
            dates.append(d[:10])
    if dates:
        try:
            return max(dates)
        except Exception:
            pass
    return datetime.now(timezone.utc).date().isoformat()


def _default_log_dates_menstruation(daily_log: Optional[List[MenstruationDailyLogInput]]) -> None:
    today_iso = datetime.now(timezone.utc).date().isoformat()
    if not daily_log:
        return
    for entry in daily_log:
        if getattr(entry, "log_date", None):
            continue
        try:
            entry.log_date = today_iso
        except Exception:
            pass


def _default_log_dates_pregnancy(daily_log: Optional[List[PregnancyDailyLogInput]]) -> None:
    today_iso = datetime.now(timezone.utc).date().isoformat()
    if not daily_log:
        return
    for entry in daily_log:
        if getattr(entry, "log_date", None):
            continue
        try:
            entry.log_date = today_iso
        except Exception:
            pass


def _dump_for_prompt(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return obj


def extract_facts(
    payload: ChatPersonaSynthesisRequest,
    *,
    today: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Send multi-session chats to Gemini and return structured factual extraction
    for downstream persona merge or bootstrap.
    """
    user_obj = {"today": today, "chats": _dump_for_prompt(payload.chats)}
    user_content = json.dumps(user_obj, indent=2, default=str, ensure_ascii=False)

    if payload.module == "M":
        system = EXTRACT_FACTS_SYSTEM_MENSTRUATION
        schema: type = MenstruationChatFactsExtraction
    else:
        system = EXTRACT_FACTS_SYSTEM_PREGNANCY
        schema = PregnancyChatFactsExtraction

    return run_gemini_json(
        system_instruction=system,
        user_content=user_content,
        output_schema=schema,
        temperature=0.25,
    )


def generate_chat_persona(
    existing_persona: Union[MenstruationPersona, PregnancyPersona],
    chat_facts: Dict[str, Any],
    daily_logs: Union[List[MenstruationDailyLogInput], List[PregnancyDailyLogInput], None],
    *,
    module: ModuleCode,
    today: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Merge existing persona with extracted chat facts and daily logs via Gemini."""
    if module == "M":
        _default_log_dates_menstruation(daily_logs if isinstance(daily_logs, list) else None)
        system = MERGE_CHAT_INTO_PERSONA_SYSTEM_MENSTRUATION
        schema = MenstruationPersonaUpdateOutput
    else:
        _default_log_dates_pregnancy(daily_logs if isinstance(daily_logs, list) else None)
        system = MERGE_CHAT_INTO_PERSONA_SYSTEM_PREGNANCY
        schema = PregnancyPersonaUpdateOutput

    body = {
        "today": today,
        "previous_persona": _dump_for_prompt(existing_persona),
        "extracted_chat_facts": chat_facts,
        "daily_logs": [_dump_for_prompt(x) for x in (daily_logs or [])],
    }
    user_content = json.dumps(body, indent=2, default=str, ensure_ascii=False)

    return run_gemini_json(
        system_instruction=system,
        user_content=user_content,
        output_schema=schema,
        temperature=0.45,
    )


def generate_new_chat_persona(
    chat_facts: Dict[str, Any],
    daily_logs: Union[List[MenstruationDailyLogInput], List[PregnancyDailyLogInput], None],
    *,
    module: ModuleCode,
    today: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Bootstrap a full persona when none exists, using chat facts and daily logs."""
    if module == "M":
        _default_log_dates_menstruation(daily_logs if isinstance(daily_logs, list) else None)
        system = NEW_PERSONA_FROM_CHAT_SYSTEM_MENSTRUATION
        schema = MenstruationPersonaUpdateOutput
    else:
        _default_log_dates_pregnancy(daily_logs if isinstance(daily_logs, list) else None)
        system = NEW_PERSONA_FROM_CHAT_SYSTEM_PREGNANCY
        schema = PregnancyPersonaUpdateOutput

    body = {
        "today": today,
        "extracted_chat_facts": chat_facts,
        "daily_logs": [_dump_for_prompt(x) for x in (daily_logs or [])],
    }
    user_content = json.dumps(body, indent=2, default=str, ensure_ascii=False)

    return run_gemini_json(
        system_instruction=system,
        user_content=user_content,
        output_schema=schema,
        temperature=0.45,
    )


async def synthesize_chat_persona(
    payload: ChatPersonaSynthesisRequest,
    user_id: Optional[str],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Orchestrate extraction, persistence reads, and persona merge or bootstrap.

    When ``user_id`` is omitted or empty, ``check_existing_persona`` and ``get_daily_logs`` are
    skipped and daily logs are treated as an empty list (bootstrap path unless you inject storage).
    """
    today = resolve_today_from_request(payload)
    facts, err = extract_facts(payload, today=today)
    if err or facts is None:
        return None, err or "extract_facts returned no data"

    uid = user_id or ""
    existing: Optional[Union[MenstruationPersona, PregnancyPersona]] = None
    if uid:
        existing = check_existing_persona(uid, module=payload.module)

    raw_logs = get_daily_logs(uid, module=payload.module) if uid else None
    daily_logs: Union[List[MenstruationDailyLogInput], List[PregnancyDailyLogInput], None]
    daily_logs = raw_logs if isinstance(raw_logs, list) else []

    if existing is not None:
        return generate_chat_persona(
            existing,
            facts,
            daily_logs,
            module=payload.module,
            today=today,
        )
    return generate_new_chat_persona(
        facts,
        daily_logs,
        module=payload.module,
        today=today,
    )
