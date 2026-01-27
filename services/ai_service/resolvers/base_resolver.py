from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseInputResolver(ABC):
    """
    Resolves backend/user data into agent-ready inputs.
    AI agents must NEVER access the database directly.
    """

    @abstractmethod
    async def resolve(
        self,
        user_id: str,
        date: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetch data using user_id and map it to agent inputs.
        Must return a dict compatible with Agent.run(**kwargs)
        """
        raise NotImplementedError
