from dataclasses import dataclass


@dataclass
class BlacklistedIP:
    host: str
    timestamp: str
    source: str
    reason: str
    definitive: bool
