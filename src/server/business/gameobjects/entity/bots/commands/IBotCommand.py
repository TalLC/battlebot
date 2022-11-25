from __future__ import annotations
from typing import Any
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=True)
class IBotCommand:
    priority: float
    action: str = field(default="action", compare=False)
    value: Any = field(default=None, compare=False)

    def __str__(self) -> str:
        return f"Priority: {self.priority} - {self.action}={self.value}"

    def execute(self, arg: BotModel) -> Any:
        """
        Contains the function to execute.
        """
        raise NotImplementedError()
