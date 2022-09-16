from consumer.webservices.messages.interfaces.IBotUpdateMessage import IBotUpdateMessage


class BotShootMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str, shoot: bool = False):
        super().__init__(bot_id=bot_id, shoot=shoot)
