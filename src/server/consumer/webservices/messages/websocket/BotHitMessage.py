from consumer.webservices.messages.websocket.interface.IBotUpdateMessage import IBotUpdateMessage


class BotHitMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str, hit: bool = False):
        super().__init__(bot_id=bot_id, hit=hit)
