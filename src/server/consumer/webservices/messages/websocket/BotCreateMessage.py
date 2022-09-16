from consumer.webservices.messages.interfaces.IBotUpdateMessage import IBotUpdateMessage


class BotCreateMessage(IBotUpdateMessage):
    def __init__(self, bot_id: str, create: bool = False):
        super().__init__(bot_id=bot_id, create=create)
