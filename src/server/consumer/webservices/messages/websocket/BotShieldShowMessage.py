from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class BotShieldShowMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, shield_show: bool = False):
        super().__init__(bot_id=bot_id, shield_show=shield_show)
