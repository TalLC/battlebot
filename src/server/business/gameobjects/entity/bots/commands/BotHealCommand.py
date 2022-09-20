from datetime import datetime
from dataclasses import dataclass, field
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand


@dataclass(order=True)
class BotHealCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="heal", compare=False)
    value: int = field(default=0, compare=False)
