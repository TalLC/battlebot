from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotMovingStatusMessage(IBotStatMessage):
    _MESSAGE_TYPE = "moving_status"

    def __init__(self, bot_id: str, moving: bool):
        super().__init__(bot_id, self._MESSAGE_TYPE, moving)
