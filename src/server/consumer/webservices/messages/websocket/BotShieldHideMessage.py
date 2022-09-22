from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class BotShieldHideMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, shield_hide: bool = False):
        super().__init__(bot_id=bot_id, shield_hide=shield_hide)
