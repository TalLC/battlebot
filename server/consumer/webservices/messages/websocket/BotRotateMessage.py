from consumer.webservices.messages.websocket.BotUpdateMessage import BotUpdateMessage


class BotRotateMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, ry: float = None):
        super().__init__(bot_id=bot_id, ry=ry)
