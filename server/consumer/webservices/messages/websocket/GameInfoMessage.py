from typing import List

from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage
from business.maps.MapName import MapName


class GameInfoMessage(IWebsocketMessage):

    @property
    def is_debug(self) -> bool:
        return self._is_debug

    @property
    def maps(self) -> List[MapName]:
        return self._maps

    @property
    def max_players(self) -> int:
        return self._max_players

    def __init__(self, is_debug: bool, maps: List[MapName], max_players: int):
        super().__init__(msg_type="GameInfoMessage")
        self._is_debug = is_debug
        self._maps = maps
        self._max_players = max_players

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        json |= {
            "is_debug": self.is_debug,
            "maps": list([map_name.json() for map_name in self.maps]),
            "max_players": self.max_players
        }
        return json
