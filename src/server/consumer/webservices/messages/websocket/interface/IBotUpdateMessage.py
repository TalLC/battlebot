from consumer.webservices.messages.websocket.interface.IBotMessage import IBotMessage


class IBotUpdateMessage(IBotMessage):

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
    def destroyed(self) -> bool:
        return self._destroyed

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

    @property
    def create(self) -> bool:
        return self._create

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None, destroyed: bool = False,
                 shoot: bool = False, hit: bool = False, shield_hide: bool = False, shield_show: bool = False,
                 create: bool = False):
        super().__init__(bot_id=bot_id)
        self._x = x
        self._z = z
        self._ry = ry
        self._destroyed = destroyed
        self._shoot = shoot
        self._hit = hit
        self._shield_hide = shield_hide
        self._shield_show = shield_show
        self._create = create

    def __add__(self, other: 'IBotUpdateMessage'):
        if self.bot_id != other.bot_id:
            raise ValueError("Bot ID must be equals!!")
        self._x = other.x if other.x is not None else self.x
        self._z = other.z if other.z is not None else self.z
        self._ry = other.ry if other.ry is not None else self.ry
        self._destroyed |= other.destroyed
        self._hit |= other.hit
        self._shoot |= other.shoot
        self._shield_hide |= other.shield_hide
        self._shield_show |= other.shield_show
        self._create |= other.create
