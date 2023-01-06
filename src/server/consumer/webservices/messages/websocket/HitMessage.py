from copy import deepcopy
from consumer.webservices.messages.websocket.interfaces.IObjectsMessage import IObjectsMessage


class HitMessage(IObjectsMessage):
    _objects: dict = dict()

    @property
    def objects(self) -> dict:
        return self._objects

    def __init__(self, object_type: str, object_id: str):
        super().__init__(msg_type="HitMessage")
        self._objects[object_type] = object_id

    def __add__(self, other):
        self._objects |= deepcopy(other.objects)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'objects': self._objects
        }
