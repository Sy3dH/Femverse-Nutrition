import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from services.ai_service.utils import prompt_templates
from services.ai_service.modules.enums import AgentName


def _dump(data: Any) -> Dict[str, Any]:
    """
    Dump a Pydantic model / arbitrary input into a plain top-level dict.
    Nested Pydantic models are recursively dumped by model_dump() / dict().
    """
    if hasattr(data, 'model_dump'):
        return data.model_dump()
    if hasattr(data, 'dict'):
        return data.dict()
    return data if isinstance(data, dict) else {}


def _derive_today(raw_context: Dict[str, Any]) -> str:
    """
    Resolve the temporal anchor (`today`, ISO-8601 YYYY-MM-DD) the LLM uses
    for every date arithmetic rule.

    Resolution order:
      1. Latest `log_date` across `daily_log` entries (if any are populated).
      2. UTC today, as a deterministic server-side default.

    The persona-update agents pass `today` explicitly when they have a more
    authoritative value (e.g. a request timestamp); this function provides the
    fallback for everyone else.
    """
    daily_log = raw_context.get("daily_log")
    if isinstance(daily_log, list):
        dates = [
            entry.get("log_date")
            for entry in daily_log
            if isinstance(entry, dict) and entry.get("log_date")
        ]
        if dates:
            try:
                # ISO-8601 YYYY-MM-DD sorts lexicographically.
                return max(dates)
            except Exception:
                pass
    return datetime.now(timezone.utc).date().isoformat()


def _format_value_for_template(value: Any) -> Any:
    """
    Render a single context value for template substitution.

    Strategy:
      - Pydantic-like values are dumped first.
      - Complex containers (dicts that contain dicts/lists, or lists of dicts)
        render as pretty JSON so the LLM receives valid JSON, not Python repr.
      - Flat dicts/lists keep the legacy shallow line-tree rendering used by
        the existing nutrition prompts.
      - Bytes are summarised.
      - Everything else is returned unchanged (the template will str() it).
    """
    if value is None:
        return value

    if hasattr(value, 'model_dump'):
        value = value.model_dump()
    elif hasattr(value, 'dict'):
        value = value.dict()

    if isinstance(value, dict):
        if any(isinstance(v, (dict, list)) for v in value.values()):
            return json.dumps(value, indent=2, default=str, ensure_ascii=False)
        return '\n'.join(f"  {k}: {v}" for k, v in value.items())

    if isinstance(value, list):
        if value and any(isinstance(item, (dict, list)) for item in value):
            return json.dumps(value, indent=2, default=str, ensure_ascii=False)
        return '\n'.join(f"  - {item}" for item in value)

    if isinstance(value, bytes):
        return f"<binary data: {len(value)} bytes>"

    return value


def _normalize_chatbot_inputs(raw_context: Dict[str, Any]) -> None:
    """
    Ensure `chatbot_inputs` never renders as the Python literal ``None``.
    A missing block becomes an explicit empty-memories object so the LLM
    sees structured emptiness rather than ambiguous null text.
    """
    if "chatbot_inputs" not in raw_context:
        return
    value = raw_context["chatbot_inputs"]
    if value is None:
        raw_context["chatbot_inputs"] = {"chatbot_memories": []}
        return
    if isinstance(value, dict) and value.get("chatbot_memories") is None:
        value["chatbot_memories"] = []


def _build_prompt_context(data: Any) -> Dict[str, Any]:
    """
    Produce the {placeholder: rendered_value} dict used by the template.
    """
    raw = _dump(data)
    _normalize_chatbot_inputs(raw)
    return {k: _format_value_for_template(v) for k, v in raw.items()}


def _get_prompt_template(agent_name: AgentName) -> Optional[str]:
    if agent_name == AgentName.NUTRITION.value:
        return prompt_templates.NUTRITION_AGENT_PROMPT

    elif agent_name == AgentName.NUTRITION_INSIGHTS.value:
        return prompt_templates.NUTRITION_INSIGHTS_PROMPT

    elif agent_name == AgentName.NUTRITION_TEXT_LOGGING.value:
        return prompt_templates.NUTRITION_TEXT_LOGGING_PROMPT

    elif agent_name == AgentName.NUTRITION_IMAGE_LOGGING.value:
        return prompt_templates.NUTRITION_IMAGE_LOGGING_PROMPT

    elif agent_name == AgentName.NUTRITION_LABEL_IMAGE_LOGGING.value:
        return prompt_templates.NUTRITION_LABEL_IMAGE_PROMPT

    # Persona agents
    elif agent_name == AgentName.MENSTRUATION_PERSONA_UPDATE.value:
        return prompt_templates.MENSTRUATION_PERSONA_UPDATE_PROMPT

    elif agent_name == AgentName.PREGNANCY_PERSONA_UPDATE.value:
        return prompt_templates.PREGNANCY_PERSONA_UPDATE_PROMPT

    elif agent_name == AgentName.NUTRITION_PERSONA_UPDATE.value:
        return prompt_templates.NUTRITION_PERSONA_UPDATE_PROMPT

    elif agent_name == AgentName.FITNESS_PERSONA_UPDATE.value:
        return prompt_templates.FITNESS_PERSONA_UPDATE_PROMPT

    # Default nutrition prompt
    return prompt_templates.NUTRITION_AGENT_PROMPT



class PromptBuilder:
    @staticmethod
    def build_prompt(
        agent_name: AgentName,
        data: Any,
        today: Optional[str] = None,
    ) -> str:
        """
        Render the final user prompt for an agent.

        The optional ``today`` argument is the ISO-8601 (YYYY-MM-DD) date the
        LLM should treat as the temporal anchor. If not supplied, it is derived
        from the latest ``log_date`` in ``data.daily_log`` and finally falls
        back to UTC today. Templates that include a ``{today}`` placeholder
        will receive this value; templates that do not are unaffected (unused
        format keys are ignored by ``str.format``).
        """
        template = _get_prompt_template(agent_name=agent_name)

        # Build the raw dict once so we can derive `today` from log_date
        # *before* the daily_log block is JSON-stringified for the prompt.
        raw = _dump(data)
        _normalize_chatbot_inputs(raw)
        resolved_today = today or _derive_today(raw)

        context = {k: _format_value_for_template(v) for k, v in raw.items()}
        context["today"] = resolved_today

        try:
            return template.format(**context)
        except KeyError as e:
            raise ValueError(f"Missing prompt variable: {e}")

    @staticmethod
    def build_template(agent_name: AgentName) -> str:

        return _get_prompt_template(agent_name=agent_name)
