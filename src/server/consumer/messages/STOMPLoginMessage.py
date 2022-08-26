from consumer.messages.interfaces.IBrokerLoginMessage import IBrokerLoginMessage


class STOMPLoginMessage(IBrokerLoginMessage):

    def __init__(self, bot_id: str, login_id: str):
        super().__init__(bot_id, login_id, 'stomp')
