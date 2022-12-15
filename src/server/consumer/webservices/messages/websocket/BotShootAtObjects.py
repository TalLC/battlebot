from copy import deepcopy
from consumer.webservices.messages.websocket.interfaces.IObjectsMessage import IObjectsMessage


class BotShootAtObjects(IObjectsMessage):
    _objects: list[str] = list()

    @property
    def objects(self) -> list[str]:
        return self._objects

    def __init__(self, bot_id: str, object_id: str):
        super().__init__(msg_type="BotShootAtObjects")
        self.bot_id = bot_id
        self._objects.append(object_id)

    def __add__(self, other):
        self._objects += deepcopy(other.objects)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'bot_id': self.bot_id,
            'objects': self.objects
        }
