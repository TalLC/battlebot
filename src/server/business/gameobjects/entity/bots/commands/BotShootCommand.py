from datetime import datetime
from dataclasses import dataclass, field
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager

from consumer.webservices.messages.websocket.BotShootMessage import BotShootMessage


@dataclass(order=True)
class BotShootCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="shoot", compare=False)
    value: float = field(default=0.0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        target = arg.shoot(self.value)
        ConsumerManager().websocket.send_message(BotShootMessage(arg.id, target))
