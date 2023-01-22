from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand

from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.BotMovingStatusMessage import BotMovingStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class BotMoveCommand(IBotCommand):
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
