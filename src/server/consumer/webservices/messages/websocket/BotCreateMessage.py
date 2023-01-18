from consumer.webservices.messages.websocket.interfaces.IBotMessage import IBotMessage


class BotCreateMessage(IBotMessage):

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
    def team_color(self) -> str:
        return self._team_color

    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None, team_color: str = str()):
        super().__init__(msg_type="BotCreateMessage", bot_id=bot_id)
        self._x = x
        self._z = z
        self._ry = ry
        self._team_color = team_color

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        return {
            'bot_id': self.bot_id,
            'msg_type': self.msg_type,
            "x": self.x,
            "z": self.z,
            "ry": self.ry,
            "team_color": self.team_color
        }
