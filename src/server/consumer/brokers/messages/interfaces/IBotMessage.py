from typing import Any
from consumer.brokers.messages.interfaces.IMessage import IMessage


class IBotMessage(IMessage):

    def __init__(self, bot_id: str, msg_type: str, data: Any, retain: bool = True):
        super().__init__(bot_id=bot_id, source='bot', msg_type=msg_type, data=data, retain=retain)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'source': self.source,
            'data': self.data
        }
