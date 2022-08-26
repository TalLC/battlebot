from abc import abstractmethod, ABC
from typing import Any


class IMessage(ABC):

    @property
    def bot_id(self) -> str:
        return self._bot_id

    @property
    def data(self) -> Any:
        return self._data

    @property
    def retain(self) -> bool:
        return self._retain

    @property
    def message(self) -> dict:
        return self._get_message()

    def __init__(self, bot_id: str, data: Any, retain: bool = False):
        self._bot_id = bot_id
        self._data = data
        self._retain = retain

    @abstractmethod
    def _get_message(self) -> dict:
        raise NotImplementedError()
