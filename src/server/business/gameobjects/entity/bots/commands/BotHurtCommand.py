from datetime import datetime
from dataclasses import dataclass, field
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager

from consumer.webservices.messages.websocket.BotHitMessage import BotHitMessage
from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage


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
        ConsumerManager().websocket.send_message(BotHitMessage(arg.id))
        ConsumerManager().stomp.send_message(BotHealthStatusMessage(arg.id, arg.health))