from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class BotHitMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, hit: bool = False):
        super().__init__(bot_id=bot_id, hit=hit)
