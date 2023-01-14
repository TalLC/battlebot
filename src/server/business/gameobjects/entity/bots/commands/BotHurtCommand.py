from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager

from consumer.webservices.messages.websocket.HitMessage import HitMessage
from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=True)
class BotHurtCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="hurt", compare=False)
    value: int = field(default=0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        arg.hurt(self.value)
        ConsumerManager().stomp.send_message(BotHealthStatusMessage(arg.id, arg.health))
