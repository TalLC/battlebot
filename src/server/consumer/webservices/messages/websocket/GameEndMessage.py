from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class GameEndMessage(IWebsocketMessage):

    @property
    def winner_name(self) -> str:
        return self._winner_name

    def __init__(self, winner_name: str):
        super().__init__(msg_type="GameEndMessage")
        self._winner_name = winner_name

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        json |= {"winner_name": self.winner_name}
        return json
