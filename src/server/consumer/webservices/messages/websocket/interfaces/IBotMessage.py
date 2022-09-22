from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class IBotMessage(IWebsocketMessage):

    @property
    def bot_id(self) -> str:
        return self._bot_id

    def __init__(self, bot_id: str):
        super().__init__()
        self._bot_id = bot_id

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        raise NotImplementedError()
