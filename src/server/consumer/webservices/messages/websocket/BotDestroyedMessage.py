from consumer.webservices.messages.websocket.interface.IBotUpdateMessage import IBotUpdateMessage


class BotDestroyedMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str):
        super().__init__(bot_id=bot_id)
