from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class MapCreateMessage(IWebsocketMessage):

    @property
    def map_id(self) -> str:
        return self._map_id

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def tiles(self) -> [dict]:
        return self._tiles

    def __init__(self, map_id: str, height: int, width: int, tiles: list):
        super().__init__(msg_type="MapCreateMessage")
        self._map_id = map_id
        self._height = height
        self._width = width
        self._tiles = tiles

    def json(self):
        return {
            'msg_type': self.msg_type,
            'id': self.map_id,
            'height': self.height,
            'width': self.width,
            'tiles': self.tiles
        }
