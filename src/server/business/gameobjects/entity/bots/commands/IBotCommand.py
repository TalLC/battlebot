from typing import Any
from dataclasses import dataclass, field


@dataclass(order=True)
class IBotCommand:
    priority: float
    action: str = field(default="action", compare=False)
    value: Any = field(default=None, compare=False)
