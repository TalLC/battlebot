from consumer.webservices.messages.websocket.interfaces.IMapMessage import IMapMessage


class MapUpdateMessage(IMapMessage):

    @property
    def tile(self) -> str:
        return self._tile

    @property
    def tile_object(self) -> str:
        return self._tile_object

    @property
    def destroyed(self) -> bool:
        return self._destroyed

    def __init__(self, x: int, z: int, tile_object: str = "", tile: str = "", destroyed: bool = False):
        super().__init__(msg_type="MapUpdateMessage", x=x, z=z)
        self._tile = tile
        self._tile_object = tile_object
        self._destroyed = destroyed

    def json(self):
        sent_json = {
            'msg_type': self.msg_type
        }
        sent_json |= {"tile": self.tile} if self.tile else dict()
        sent_json |= {"tile_object": self.tile_object} if self.tile_object else dict()
        sent_json |= {"destroyed": self.destroyed} if self.destroyed else dict()
        return sent_json
