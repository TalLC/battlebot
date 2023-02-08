from consumer.webservices.messages.websocket.interfaces.IObjectMessage import IObjectMessage


class GameObjectHurtMessage(IObjectMessage):

    def __init__(self, object_id: str):
        super().__init__(msg_type="GameObjectHurtMessage", object_id=object_id)

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        return super().json()

