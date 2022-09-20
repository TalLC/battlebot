from datetime import datetime
from dataclasses import dataclass


@dataclass
class IPLog:
    host: str
    timestamp: datetime
    source: str
