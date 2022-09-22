from consumer.webservices.messages.websocket.interfaces.IBotMessage import IBotMessage
from consumer.webservices.messages.websocket.models.EnumStatus import EnumStatus
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
    def action(self) -> EnumStatus:
        return self._action

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None,
                 target: Target = None, action: EnumStatus = EnumStatus.NONE):
        super().__init__(msg_type="BotUpdateMessage", bot_id=bot_id)
        self._x = x
        self._z = z
        self._targets = [target] if target is not None else list()
        self._ry = ry
        self._action = action

    def __add__(self, other: 'BotUpdateMessage'):
        if self.bot_id != other.bot_id:
            raise ValueError("Bot ID must be equals!!")
        self._x = other.x if other.x is not None else self.x
        self._z = other.z if other.z is not None else self.z
        self._ry = other.ry if other.ry is not None else self.ry
        self._targets += other.targets if len(other.targets) > 0 else list()
        self._action |= other.action

    def json(self) -> dict:
        sent_json = {
            'bot_id': self.bot_id,
            'msg_type': self.msg_type
        }
        sent_json |= {"x": self.x} if self.x else dict()
        sent_json |= {"z": self.z} if self.z else dict()
        sent_json |= {"ry": self.ry} if self.ry else dict()
        sent_json |= {"targets": [t.json() for t in self.targets]} if len(self.targets) else dict()
        sent_json |= {"action": self.action.value}
        return sent_json
