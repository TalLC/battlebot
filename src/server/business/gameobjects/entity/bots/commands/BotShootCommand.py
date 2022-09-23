from datetime import datetime
from dataclasses import dataclass, field

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand


@dataclass(order=True)
class BotShootCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="shoot", compare=False)
    value: float = field(default=0.0, compare=False)
