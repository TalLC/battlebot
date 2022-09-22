from consumer.webservices.messages.websocket.models.EnumStatus import EnumStatus
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
    def action(self) -> EnumStatus:
        return self._action

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None,
                 action: EnumStatus = EnumStatus.NONE):
        super().__init__(bot_id=bot_id)
        self._x = x
        self._z = z
        self._ry = ry
        self._action = action

    def __add__(self, other: 'BotUpdateMessage'):
        if self.bot_id != other.bot_id:
            raise ValueError("Bot ID must be equals!!")
        self._x = other.x if other.x is not None else self.x
        self._z = other.z if other.z is not None else self.z
        self._ry = other.ry if other.ry is not None else self.ry
        self._action |= other.action

    def json(self) -> dict:
        sent_json = {}
        sent_json |= {"x": self.x} if self.x else dict()
        sent_json |= {"z": self.z} if self.z else dict()
        sent_json |= {"ry": self.ry} if self.ry else dict()
        sent_json |= {"action": self.action.value}
        return sent_json
