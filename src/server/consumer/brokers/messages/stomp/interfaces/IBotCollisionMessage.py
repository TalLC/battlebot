from typing import Any
from consumer.brokers.messages.interfaces.IBotMessage import IBotMessage


class IBotCollisionMessage(IBotMessage):

    def __init__(self, bot_id: str, msg_type: str, stat_value: Any):
        data = {
            "collision_with": stat_value
        }
        super().__init__(bot_id=bot_id, source="bot", msg_type=msg_type, data=data)
