from consumer.webservices.messages.websocket.interface.IBotUpdateMessage import IBotUpdateMessage


class BotDestroyedMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str, destroyed: bool = False):
        super().__init__(bot_id=bot_id, destroyed=destroyed)
