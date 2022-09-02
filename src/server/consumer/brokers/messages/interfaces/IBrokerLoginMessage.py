from consumer.messages.interfaces.IMessage import IMessage


class IBrokerLoginMessage(IMessage):

    @property
    def login_id(self):
        return self._login_id

    @property
    def broker_name(self):
        return self._broker_name

    def __init__(self, bot_id: str, login_id: str, broker_name: str, retain: bool = False):
        self._login_id = login_id
        self._broker_name = broker_name
        super().__init__(bot_id, {f"{broker_name.lower()}_id": login_id}, retain)

    def _get_message(self) -> dict:
        return self.data
