from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand

from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class BotHurtCommand(IBotCommand):
    action: str = field(default="hurt", compare=False)
    value: int = field(default=0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        arg.hurt(self.value)
        ConsumerManager().stomp.send_message(BotHealthStatusMessage(arg.id, arg.health))
