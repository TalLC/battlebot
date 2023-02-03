from abc import ABC
from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class IObjectMessage(IWebsocketMessage, ABC):

    @property
    def id(self) -> str:
        return self._id

    def __init__(self, msg_type: str, object_id: str):
        super().__init__(msg_type)
        self._id = object_id

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        json |= {'id': self.id}
        return json
