from __future__ import annotations
from consumer.webservices.messages.websocket.interfaces.IBotMessage import IBotMessage
from consumer.webservices.messages.websocket.models.Target import Target


class BotUpdateMessage(IBotMessage):

    @property
    def x(self) -> float:
        return self._x

    @property
    def z(self) -> float:
        return self._z

    @property
    def targets(self) -> list:
        return self._targets

    @property
    def ry(self) -> float:
        return self._ry

    @property
    def hit(self) -> bool:
        return self._hit

    @property
    def shield(self) -> bool:
        return self._shield

    @property
    def data(self) -> dict:
        return self._data

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None,
                 target: Target = None, hit: bool = False, shield: bool = None):
        super().__init__(msg_type="BotUpdateMessage", bot_id=bot_id)
        self._x = x
        self._z = z
        self._targets = [target] if target is not None else list()
        self._ry = ry
        self._shield = shield
        self._hit = hit
        self._data = {
            "bot_id": bot_id,
            "move": {"x": x, "z": z},
            "rotate": {"ry": ry},
            "shoot": self._targets,
            "hit": {"status": hit},
            "shield": {"status": shield}
        }

    def __add__(self, other: BotUpdateMessage):
        if self.bot_id != other.bot_id:
            raise ValueError("Bot ID must be equals!!")
        self._x = other.x if other.x is not None else self.x
        self._z = other.z if other.z is not None else self.z
        self._ry = other.ry if other.ry is not None else self.ry
        self._targets += other.targets if len(other.targets) > 0 else list()
        self._shield = other.shield if other.shield is not None else self.shield
        self._hit = other.hit if other.hit is not False else self.hit
        self._data = {
            "bot_id": self.bot_id,
            "move": {"x": self._x, "z": self._z},
            "rotate": {"ry": self._ry},
            "shoot": self._targets,
            "hit": {"status": self._hit},
            "shield": {"status": self._shield}
        }

    @staticmethod
    def formate_data(data: dict) -> dict:
        result = {"bot_id": data["bot_id"],
                  "move": data["move"] if data["move"]["x"] is not None or data["move"]["z"] is not None else None,
                  "rotate": data["rotate"] if data["rotate"]["ry"] is not None else None,
                  "shoot": data["shoot"] if data["shoot"] else None,
                  "hit": data["hit"] if data["hit"]["status"] else None,
                  "shield": data["shield"] if data["shield"]["status"] is not None else None}

        for k, v in result.copy().items():
            if v is None:
                del result[k]
        return result

    def json(self) -> dict:
        sent_json = {
            'msg_type': self.msg_type,
            'data': self.formate_data(self._data)
        }
        return sent_json
