from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand

from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.BotTurningStatusMessage import BotTurningStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class BotTurnCommand(IBotCommand):
    action: str = field(default="turn", compare=False)
    value: str = field(default=str(), compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        if self.value == "stop":
            arg.set_turning(False)
        else:
            arg.set_turning(True, self.value)
        ConsumerManager().stomp.send_message(BotTurningStatusMessage(arg.id, self.value))
