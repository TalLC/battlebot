from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotTurningStatusMessage(IBotStatMessage):
    _MESSAGE_TYPE = "turning_status"

    def __init__(self, bot_id: str, turning: str):
        super().__init__(bot_id, self._MESSAGE_TYPE, turning)
