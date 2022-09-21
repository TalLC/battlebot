from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class IMapMessage(IWebsocketMessage):

    @property
    def x(self) -> int:
        return self._x

    @property
    def z(self) -> int:
        return self._z

    def __init__(self, x: int, z: int):
        super().__init__(x=x, z=z)
        self._x = x
        self._z = z
