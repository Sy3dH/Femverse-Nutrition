import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple

from services.ai_service.base_agent import BaseAgent
from services.ai_service.modules.persona.models import MenstruationPersonaUpdateInput
from services.ai_service.modules.persona.models import MenstruationPersonaUpdateOutput
from services.ai_service.modules.enums import AgentName
from services.ai_service.utils.prompt_builder import PromptBuilder

logger = logging.getLogger("celery")


class MenstruationPersonaAgent(BaseAgent):
    """
    Agent for updating menstruation user persona based on daily logs.
    Synthesizes daily health data into a long-term health narrative.

    The same agent class backs both the SINGLE-LOG and BATCH-LOG agent-name
    variants. The route layer is responsible for picking the right variant
    (and therefore the right cached system prompt) before dispatching.
    """

    DEFAULT_AGENT_NAME = AgentName.MENSTRUATION_PERSONA_UPDATE_SINGLE.value

    @staticmethod
    def _resolve_today(inputs: MenstruationPersonaUpdateInput) -> str:
        """
        Pick the latest `log_date` from the daily log as the authoritative
        "today" anchor for date arithmetic; fall back to UTC today if every
        entry omits it.
        """
        try:
            dates = [
                entry.log_date
                for entry in (inputs.daily_log or [])
                if getattr(entry, "log_date", None)
            ]
            if dates:
                return max(dates)
        except Exception:
            pass
        return datetime.now(timezone.utc).date().isoformat()

    @staticmethod
    def _sort_daily_log_ascending(inputs: MenstruationPersonaUpdateInput) -> None:
        """
        Sort `daily_log` in place by `log_date` ascending so the BATCH-LOG
        system prompt's "pre-sorted by log_date ascending" guarantee holds
        regardless of the order in which the route layer received entries.

        Entries without a `log_date` sort first (they're treated as the
        oldest, since the route layer already defaulted missing dates to
        the request `today`).
        """
        if not inputs.daily_log:
            return
        try:
            inputs.daily_log.sort(
                key=lambda entry: getattr(entry, "log_date", "") or ""
            )
        except Exception:
            logger.warning(
                "MenstruationPersonaAgent: failed to sort daily_log ascending; "
                "passing through original order"
            )

    @staticmethod
    def _resolve_prev_last_updated(inputs: MenstruationPersonaUpdateInput) -> str:
        """
        Return the ISO date the persona was last persisted, or the literal
        string ``"Unknown"`` if the previous persona has no `last_updated`.
        Surfaced in the prompt so the LLM can apply the DATE CONTRACT's
        "low engagement gap" rule without having to hunt through the JSON.
        """
        try:
            prev = getattr(inputs, "previous_persona", None)
            if prev is not None and getattr(prev, "last_updated", None):
                return prev.last_updated
        except Exception:
            pass
        return "Unknown"

    async def run(
        self,
        inputs: MenstruationPersonaUpdateInput,
        cached_content_name: Optional[str] = None,
        agent_name: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            today = self._resolve_today(inputs)
            prev_last_updated = self._resolve_prev_last_updated(inputs)
            self._sort_daily_log_ascending(inputs)

            user_prompt = PromptBuilder.build_prompt(
                agent_name=agent_name or self.DEFAULT_AGENT_NAME,
                data=inputs,
                today=today,
                extra_context={"prev_last_updated": prev_last_updated},
            )

            response, error = self.query_llm(
                prompt=user_prompt,
                output_schema=MenstruationPersonaUpdateOutput,
                cached_content_name=cached_content_name,
            )

            if error:
                logger.error(f"MenstruationPersonaAgent LLM error: {error}")
                return None, error

            return response, None

        except Exception as e:
            logger.exception("MenstruationPersonaAgent failed")
            return None, str(e)
