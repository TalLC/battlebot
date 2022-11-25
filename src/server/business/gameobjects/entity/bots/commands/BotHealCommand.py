from datetime import datetime
from dataclasses import dataclass, field
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager

from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage


@dataclass(order=True)
class BotHealCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="heal", compare=False)
    value: int = field(default=0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        arg.heal(self.value)
        ConsumerManager().stomp.send_message(BotHealthStatusMessage(arg.id, arg.health))
