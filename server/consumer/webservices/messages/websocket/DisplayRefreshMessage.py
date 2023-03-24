from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class DisplayRefreshMessage(IWebsocketMessage):

    def __init__(self):
        super().__init__(msg_type="DisplayRefreshMessage")

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        return json
