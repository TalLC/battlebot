from consumer.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotHealthStatusMessage(IBotStatMessage):
    _MESSAGE_TYPE = "health_status"

    def __init__(self, bot_id: str, health: int):
        super().__init__(bot_id, self._MESSAGE_TYPE, health)
