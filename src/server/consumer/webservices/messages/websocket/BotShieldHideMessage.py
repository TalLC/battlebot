from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage
from consumer.webservices.messages.websocket.models.EnumStatus import EnumStatus


class BotShieldHideMessage(BotUpdateMessage):
    def __init__(self, bot_id: str):
        super().__init__(bot_id=bot_id, action=EnumStatus.SHIELD_HIDE)
