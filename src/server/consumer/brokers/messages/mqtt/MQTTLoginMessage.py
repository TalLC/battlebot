from consumer.brokers.messages.interfaces.IBrokerLoginMessage import IBrokerLoginMessage


class MQTTLoginMessage(IBrokerLoginMessage):

    def __init__(self, bot_id: str, login_id: str):
        super().__init__(bot_id=bot_id, login_id=login_id, broker_name='mqtt', retain=True)
