from consumer.webservices.messages.websocket.BotUpdateMessage import BotUpdateMessage


class BotMoveMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, x: float = None, z: float = None):
        super().__init__(bot_id=bot_id, x=x, z=z)
