from typing import Any
from consumer.messages.interfaces.ISensorMessage import ISensorMessage


class IScannerMessage(ISensorMessage):
    _SENSOR = "Scanner"

    def __init__(self, bot_id: str, info_type: str, data: Any):
        super().__init__(bot_id, self._SENSOR, info_type, data)
