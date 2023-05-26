from abc import ABC
from time import time
from typing import Any


class IMessage(ABC):

    @property
    def bot_id(self) -> str:
        return self._bot_id

    @property
    def source(self) -> str:
        return self._source

    @property
    def msg_type(self) -> str:
        return self._msg_type

    @property
    def data(self) -> Any:
        return self._data

    @property
    def retain(self) -> bool:
        return self._retain

    def __init__(self, bot_id: str, source: str, msg_type: str, data: Any, retain: bool = False):
        self._bot_id = bot_id
        self._source = source
        self._msg_type = msg_type
        self._data = data
        self._retain = retain

    def json(self) -> dict:
        return {
           'timestamp': time()
        }
