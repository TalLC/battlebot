from consumer.webservices.messages.websocket.interfaces.IMapMessage import IMapMessage


class MapUpdateMessage(IMapMessage):

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

    def json(self):
        sent_json = {}
        sent_json |= {"create_object": self.create_object} if self.create_object else None
        sent_json |= {"create_tile": self.create_tile} if self.create_tile else None
        sent_json |= {"destroyed": self.destroyed} if self.destroyed else None
        return sent_json
