from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager

from consumer.brokers.messages.stomp.BotStunningStatusMessage import BotStunningStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=True)
class BotStunCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="stun", compare=False)
    value: float = field(default=0.0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        arg.stun()
        if arg.is_moving:
            arg.add_command_to_queue(BotMoveCommand(priority=0, value='stop'))
