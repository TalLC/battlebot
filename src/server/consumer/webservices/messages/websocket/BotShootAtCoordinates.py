from copy import deepcopy
from consumer.webservices.messages.websocket.interfaces.ICoordinatesMessage import ICoordinatesMessage


class BotShootAtCoordinates(ICoordinatesMessage):
    _coordinates: list[dict] = list()

    def coordinates(self):
        return self._coordinates

    def __init__(self, bot_id: str, hit_x: float, hit_z: float):
        super().__init__(msg_type="BotShootAtCoordinates")
        self.bot_id = bot_id
        self._coordinates.append(
            {'x': hit_x, 'z': hit_z}
        )

    def __add__(self, other):
        self._coordinates += deepcopy(other.coordinates)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'bot_id': self.bot_id,
            'coordinates': self._coordinates
        }
