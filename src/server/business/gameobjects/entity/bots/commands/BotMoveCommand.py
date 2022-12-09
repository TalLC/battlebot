from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.BotMovingStatusMessage import BotMovingStatusMessage


if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class BotMoveCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="move", compare=False)
    value: str = field(default=str(), compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        if self.value == "stop":
            arg.set_moving(False)
        else:
            arg.set_moving(True)
        ConsumerManager().stomp.send_message(BotMovingStatusMessage(arg.id, arg.is_moving))

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
