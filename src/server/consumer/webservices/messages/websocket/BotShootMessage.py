from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage
from consumer.webservices.messages.websocket.models.EnumStatus import EnumStatus
from consumer.webservices.messages.websocket.models.Target import Target


class BotShootMessage(BotUpdateMessage):
    def __init__(self, bot_id: str, target: Target):
        super().__init__(bot_id=bot_id, target=target, action=EnumStatus.SHOOTING)
