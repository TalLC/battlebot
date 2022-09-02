from typing import Any
from consumer.brokers.messages.interfaces.IBotMessage import IBotMessage


class IBotStatMessage(IBotMessage):
    _SOURCE = "bot"

    def __init__(self, bot_id: str, message_type: str, stat_value: Any):
        data = {"value": stat_value}
        super().__init__(bot_id, self._SOURCE, message_type, data)
