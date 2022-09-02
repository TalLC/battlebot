from typing import Any
from consumer.messages.interfaces.IBotMessage import IBotMessage


class IShieldMessage(IBotMessage):
    _SOURCE = "shield"

    def __init__(self, bot_id: str, message_type: str, data: Any):
        super().__init__(bot_id, self._SOURCE, message_type, data)