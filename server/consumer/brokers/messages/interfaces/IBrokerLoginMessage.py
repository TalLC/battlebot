from time import time
from consumer.brokers.messages.interfaces.IMessage import IMessage


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
        data = {
            "value": login_id
        }

        super().__init__(bot_id=bot_id, source='server', msg_type=f"{broker_name.lower()}_id", data=data, retain=retain)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'timestamp': time(),
            'source': self.source,
            'data': self.data
        }
