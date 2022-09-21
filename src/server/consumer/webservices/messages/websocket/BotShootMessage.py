from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class BotShootMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, shoot: bool = False):
        super().__init__(bot_id=bot_id, shoot=shoot)
