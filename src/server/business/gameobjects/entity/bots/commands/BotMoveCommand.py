from datetime import datetime
from dataclasses import dataclass, field

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand


@dataclass(order=True)
class BotMoveCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="move", compare=False)
    value: str = field(default=str(), compare=False)
