from business.displays.DisplayClient import DisplayClient
from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class DisplayClientLoginMessage(IWebsocketMessage):

    @property
    def login_id(self):
        return self._login_id

    @property
    def client_name(self):
        return self._client_name

    def __init__(self, display_client: DisplayClient):
        self._login_id = display_client.login_id
        self._client_name = display_client.name
        super().__init__(msg_type=f"DisplayClientLoginMessage")

    def json(self):
        return {
            'msg_type': self.msg_type,
            'client_name': self._client_name,
            'login_id': self._login_id
        }
