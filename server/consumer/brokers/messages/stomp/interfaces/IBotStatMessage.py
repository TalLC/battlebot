from typing import Any
from consumer.brokers.messages.interfaces.IBotMessage import IBotMessage


class IBotStatMessage(IBotMessage):

    def __init__(self, bot_id: str, msg_type: str, stat_value: Any):
        data = {
            "value": stat_value
        }
        super().__init__(bot_id=bot_id, msg_type=msg_type, data=data)