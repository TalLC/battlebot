from consumer.webservices.messages.websocket.interface.IBotUpdateMessage import IBotUpdateMessage


class BotCreateMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str, x: float = None, z: float = None, ry: float = None):
        super().__init__(bot_id=bot_id, x=x, z=z, ry=ry)
