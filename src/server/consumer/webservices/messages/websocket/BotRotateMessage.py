from consumer.webservices.messages.interfaces.IBotUpdateMessage import IBotUpdateMessage


class BotRotateMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str, ry: float = None):
        super().__init__(bot_id=bot_id, ry=ry)
