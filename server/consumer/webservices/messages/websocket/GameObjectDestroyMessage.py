from consumer.webservices.messages.websocket.interfaces.IObjectMessage import IObjectMessage


class GameObjectDestroyMessage(IObjectMessage):

    def __init__(self, object_id: str):
        super().__init__(msg_type="GameObjectDestroyMessage", object_id=object_id)

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        return super().json()
