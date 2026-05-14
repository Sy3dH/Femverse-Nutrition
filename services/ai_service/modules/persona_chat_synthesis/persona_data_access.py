from __future__ import annotations

from typing import List, Optional, Union

from services.ai_service.modules.persona.models import (
    MenstruationDailyLogInput,
    MenstruationPersona,
    PregnancyDailyLogInput,
    PregnancyPersona,
)


def check_existing_persona(
    user_id: str,
    *,
    module: str,
) -> Optional[Union[MenstruationPersona, PregnancyPersona]]:
    """
    Load the latest persisted long-term persona for ``user_id`` for the active module.

    Parameters
    ----------
    user_id:
        Stable user identifier from the API layer.
    module:
        ``\"M\"`` for menstruation persona, ``\"P\"`` for pregnancy persona.

    Returns
    -------
    MenstruationPersona | PregnancyPersona | None
        The most recent stored persona document, or ``None`` if none exists
        (caller should bootstrap via ``generate_new_chat_persona``).

    Notes
    -----
    Persistence (database, cache, object storage) is owned by the backend team.
    """
    # TODO: Implement backend logic init
    pass


def get_daily_logs(
    user_id: str,
    *,
    module: str,
) -> Optional[Union[List[MenstruationDailyLogInput], List[PregnancyDailyLogInput]]]:
    """
    Fetch recent daily log entries for ``user_id`` for the active module.

    Parameters
    ----------
    user_id:
        Stable user identifier from the API layer.
    module:
        ``\"M\"`` → ``MenstruationDailyLogInput`` list; ``\"P\"`` → ``PregnancyDailyLogInput`` list.

    Returns
    -------
    list | None
        Chronological or reverse-chronological daily logs (contract TBD with storage).
        Return an empty list when there are no logs. ``None`` may be coerced to ``[]`` by callers.

    Notes
    -----
    Windowing (e.g. last 30 days, since last persona update) is implementation-defined.
    """
    # TODO: Implement backend logic init
    pass
