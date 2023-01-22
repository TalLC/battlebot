from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand

from consumer.ConsumerManager import ConsumerManager
from consumer.webservices.messages.websocket.BotShootAtObjects import BotShootAtObjects
from consumer.webservices.messages.websocket.BotShootAtCoordinates import BotShootAtCoordinates

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class BotShootCommand(IBotCommand):
    action: str = field(default="shoot", compare=False)
    value: float = field(default=0.0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        target = arg.shoot(self.value)
        if target.id:
            ConsumerManager().websocket.send_message(BotShootAtObjects(arg.id, target.id))
        else:
            ConsumerManager().websocket.send_message(BotShootAtCoordinates(arg.id, {'x': target.x, 'y': target.z}))
