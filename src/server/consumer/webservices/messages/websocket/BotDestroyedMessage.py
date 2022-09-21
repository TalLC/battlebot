from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class BotDestroyedMessage(BotUpdateMessage):
    def __init__(self, bot_id: str):
        super().__init__(bot_id=bot_id)
