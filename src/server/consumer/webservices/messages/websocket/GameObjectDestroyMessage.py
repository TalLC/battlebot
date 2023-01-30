from consumer.webservices.messages.websocket.interfaces.IObjectMessage import IObjectMessage


class MapObjectDestroyMessage(IObjectMessage):

    def __init__(self, object_id: str):
        super().__init__(msg_type="MapObjectDestroyMessage", object_id=object_id)

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'id': self.id
        }
