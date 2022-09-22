from datetime import datetime
from dataclasses import dataclass, field
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand


@dataclass(order=True)
class BotHurtCommand(IBotCommand):
    priority: float = float(datetime.now().timestamp())
    action: str = field(default="hurt", compare=False)
    value: int = field(default=0, compare=False)
