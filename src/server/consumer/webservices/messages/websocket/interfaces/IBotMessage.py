from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class IBotMessage(IWebsocketMessage):

    @property
    def bot_id(self) -> str:
        return self._bot_id

    def __init__(self, msg_type: str, bot_id: str):
        super().__init__(msg_type)
        self._bot_id = bot_id

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'bot_id': self.bot_id
        }
