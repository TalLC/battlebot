from typing import Any
from consumer.messages.interfaces.IMessage import IMessage


class ISensorMessage(IMessage):
    _SENSOR = str()
    _INFO_TYPE = str()

    @property
    def sensor(self) -> str:
        return self._SENSOR

    @property
    def info_type(self):
        return self._INFO_TYPE

    def __init__(self, bot_id: str, sensor: str, info_type: str, data: Any, retain: bool = True):
        self._SENSOR = sensor
        self._INFO_TYPE = info_type
        super().__init__(bot_id, data, retain)

    def _get_message(self) -> dict:
        message = dict()
        message['sensor'] = self.sensor
        message['type'] = self.info_type
        message['data'] = self.data
        return message
