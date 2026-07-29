from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Skill(ABC):
    """Contract shared by executable procurement skills."""

    name: str
    version: str
    description: str

    @abstractmethod
    async def execute(
        self,
        inputs: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute the skill with a transport-neutral input dictionary."""
