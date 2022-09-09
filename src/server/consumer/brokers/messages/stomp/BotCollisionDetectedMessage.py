from consumer.brokers.messages.stomp.interfaces.IBotCollisionMessage import IBotCollisionMessage


class BotCollisionDetectedMessage(IBotCollisionMessage):
    _MESSAGE_TYPE = "collision_detected"

    def __init__(self, bot_id: str, object_name: str):
        super().__init__(bot_id, self._MESSAGE_TYPE, object_name)
