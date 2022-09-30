from datetime import datetime
from dataclasses import dataclass, field
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.ConsumerManager import ConsumerManager

from consumer.brokers.messages.stomp.BotMovingStatusMessage import BotMovingStatusMessage


@dataclass(order=True)
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
