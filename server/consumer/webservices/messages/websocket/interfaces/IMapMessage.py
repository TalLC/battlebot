from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class IMapMessage(IWebsocketMessage):

    @property
    def x(self) -> int:
        return self._x

    @property
    def z(self) -> int:
        return self._z

    def __init__(self, msg_type: str, x: int, z: int):
        super().__init__(msg_type=msg_type)
        self._x = x
        self._z = z

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'x': self.x,
            'z': self.z
        }
