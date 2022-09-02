from typing import Any
from consumer.brokers.messages.interfaces.IMessage import IMessage


class IBotMessage(IMessage):
    _SOURCE = str()
    _MESSAGE_TYPE = str()

    @property
    def source(self) -> str:
        return self._SOURCE

    @property
    def message_type(self):
        return self._MESSAGE_TYPE

    def __init__(self, bot_id: str, source: str, message_type: str, data: Any, retain: bool = True):
        self._SOURCE = source
        self._MESSAGE_TYPE = message_type
        super().__init__(bot_id, data, retain)

    def _get_message(self) -> dict:
        message = dict()
        message['source'] = self.source
        message['type'] = self.message_type
        message['data'] = self.data
        return message
