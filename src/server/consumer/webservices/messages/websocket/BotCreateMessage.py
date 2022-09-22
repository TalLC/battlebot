from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class BotCreateMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None):
        super().__init__(bot_id=bot_id, x=x, z=z, ry=ry)
