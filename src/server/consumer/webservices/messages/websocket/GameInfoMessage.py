from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class GameInfoMessage(IWebsocketMessage):

    @property
    def is_debug(self) -> bool:
        return self._is_debug

    @property
    def map_id(self) -> str:
        return self._map_id

    @property
    def max_players(self) -> int:
        return self._max_players

    def __init__(self, is_debug: bool, map_id: str, max_players: int):
        super().__init__(msg_type="GameInfoMessage")
        self._is_debug = is_debug
        self._map_id = map_id
        self._max_players = max_players

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        json |= {
            "is_debug": self.is_debug,
            "map_id": self.map_id,
            "max_players": self.max_players
        }
        return json
