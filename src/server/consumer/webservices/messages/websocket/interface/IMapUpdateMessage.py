from consumer.webservices.messages.websocket.interface.IMapMessage import IMapMessage


class IMapUpdateMessage(IMapMessage):

    @property
    def create_object(self) -> str:
        return self._create_object

    @property
    def create_tile(self) -> str:
        return self._create_tile

    @property
    def destroyed(self) -> bool:
        return self._destroyed

    def __init__(self, x: int, z: int, create_object: str = "", create_tile: str = "", destroyed: bool = False):
        super().__init__(x, z)
        self._create_object = create_object
        self._create_tile = create_tile
        self._destroyed = destroyed

    # def __add__(self, other: 'IMapUpdateMessage'):
        # if self.x != other.x or self.z != other.z:
        #     raise ValueError("Coordinate must be equals!!")
        # self._x = other.x if other.x is not None else self.x
        # self._z = other.z if other.z is not None else self.z
        # self._create_object = other.create_object if other.create_object is not "" else self.create_object
        # self._create_tile = other.create_tile if other.create_tile is not "" else self.create_tile
        # self._destroyed |= other.destroyed
