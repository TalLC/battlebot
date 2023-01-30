from abc import abstractmethod, ABC


class IWebsocketMessage(ABC):

    @property
    def msg_type(self) -> str:
        return self._msg_type

    def __init__(self, msg_type: str):
        self._msg_type = msg_type

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type
        }
