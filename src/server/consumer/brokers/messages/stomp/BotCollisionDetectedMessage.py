from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotCollisionDetectedMessage(IBotStatMessage):
    _MESSAGE_TYPE = "collision_detected"

    def __init__(self, bot_id: str):
        super().__init__(bot_id, self._MESSAGE_TYPE, True)
