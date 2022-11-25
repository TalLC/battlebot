from typing import Any
from consumer.brokers.messages.interfaces.IMessage import IMessage


class IBotMessage(IMessage):

    @property
    def source(self) -> str:
        return self._source

    def __init__(self, bot_id: str, source: str, msg_type: str, data: Any, retain: bool = True):
        self._source = source
        super().__init__(bot_id=bot_id, msg_type=msg_type, data=data, retain=retain)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'source': self.source,
            'data': self.data
        }
