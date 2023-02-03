from __future__ import annotations
from consumer.webservices.messages.websocket.interfaces.IObjectMessage import IObjectMessage
from consumer.webservices.messages.websocket.models.Target import Target


class BotUpdateMessage(IObjectMessage):

    @property
    def x(self) -> float:
        return self._x

    @property
    def z(self) -> float:
        return self._z

    @property
    def ry(self) -> float:
        return self._ry

    @property
    def targets(self) -> list:
        return self._targets

    @property
    def shield(self) -> bool:
        return self._shield

    @property
    def hit(self) -> bool:
        return self._hit

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None,
                 target: Target = None, shield: bool = None, hit: bool = False):
        super().__init__(msg_type="BotUpdateMessage", object_id=bot_id)
        self._x = x
        self._z = z
        self._ry = ry
        self._targets = [target.json()] if target is not None else list()
        self._shield = shield
        self._hit = hit

    def __add__(self, other: BotUpdateMessage):
        if self.id != other.id:
            raise ValueError("Bot ID must be equals!!")
        self._x = other.x if other.x is not None else self.x
        self._z = other.z if other.z is not None else self.z
        self._ry = other.ry if other.ry is not None else self.ry
        self._targets += other.targets if len(other.targets) > 0 else list()
        self._shield = other.shield if other.shield is not None else self.shield
        self._hit = other.hit if other.hit else self.hit

    def json(self) -> dict:
        json = super().json()
        # json = {'msg_type': self.msg_type, "id": self.id}
        if self.x or self.z:
            json['move'] = dict()
            json['move'] |= {'x': self.x} if self.x is not None else dict()
            json['move'] |= {'z': self.z} if self.z is not None else dict()
        json |= {'rotate': {'ry': self.ry}} if self.ry is not None else dict()
        json |= {'shoot': self.targets} if len(self.targets) > 0 else dict()
        json |= {'shield': {'status': self.shield}} if self.shield is not None else dict()
        json |= {'hit': {'status': self.hit}} if self.hit else dict()
        return json
