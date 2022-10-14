from typing import Any
from consumer.brokers.messages.interfaces.IBotMessage import IBotMessage


class IShieldMessage(IBotMessage):

    def __init__(self, bot_id: str, msg_type: str, data: Any):
        super().__init__(bot_id=bot_id, source="shield", msg_type=msg_type, data=data)
