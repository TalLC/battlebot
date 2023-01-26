from __future__ import annotations
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class IBotCommand:
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="action", compare=False)
    value: Any = field(default=None, compare=False)

    def __str__(self) -> str:
        return f"Priority: {self.priority} - {self.action}={self.value}"

    def execute(self, arg: BotModel) -> Any:
        """
        Contains the function to execute.
        """
        raise NotImplementedError()

    # Todo : Utiliser l'ordonnancement des Dataclass avec une comparaison d'instances différents si c'est possible
    #  en python 3
    def __lt__(self, other):
        if isinstance(other, IBotCommand):
            return self.priority < other.priority
        else:
            return TypeError(f"'<' not supported between instances of '{type(self)}' and '{type(other)}'")

    def __gt__(self, other):
        if isinstance(other, IBotCommand):
            return self.priority > other.priority
        else:
            return TypeError(f"'>' not supported between instances of '{type(self)}' and '{type(other)}'")
