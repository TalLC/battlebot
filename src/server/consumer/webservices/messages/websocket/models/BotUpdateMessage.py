from consumer.webservices.messages.websocket.EnumStatus import EnumStatus
from consumer.webservices.messages.websocket.interfaces.IBotMessage import IBotMessage


class BotUpdateMessage(IBotMessage):

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
    def shoot(self) -> bool:
        return self._shoot

    @property
    def hit(self) -> bool:
        return self._hit

    @property
    def shield_hide(self) -> bool:
        return self._shield_hide

    @property
    def shield_show(self) -> bool:
        return self._shield_show

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None,
                 shoot: bool = False, hit: bool = False, shield_hide: bool = False, shield_show: bool = False):
        super().__init__(bot_id=bot_id)
        self._x = x
        self._z = z
        self._ry = ry
        self._shoot = shoot
        self._hit = hit
        self._shield_hide = shield_hide
        self._shield_show = shield_show

    def __add__(self, other: 'BotUpdateMessage'):
        if self.bot_id != other.bot_id:
            raise ValueError("Bot ID must be equals!!")
        self._x = other.x if other.x is not None else self.x
        self._z = other.z if other.z is not None else self.z
        self._ry = other.ry if other.ry is not None else self.ry
        self._hit |= other.hit
        self._shoot |= other.shoot
        self._shield_hide |= other.shield_hide
        self._shield_show |= other.shield_show

    def json(self) -> dict:
        sent_json = {}
        sent_json |= {"x": self.x} if self.x else None
        sent_json |= {"z": self.z} if self.z else None
        sent_json |= {"ry": self.ry} if self.ry else None
        sent_json |= {"hit": self.hit} if self.hit else None
        sent_json |= {"shoot": self.shoot} if self.shoot else None
        sent_json |= {"shield_hide": self.shield_hide} if self.shield_hide else None
        sent_json |= {"shield_show": self.shield_show} if self.shield_show else None
        return sent_json
