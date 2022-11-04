from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotCollisionDetectedMessage(IBotStatMessage):

    def __init__(self, bot_id: str, object_name: str):
        super().__init__(bot_id=bot_id, msg_type="collision_detected", stat_value=object_name)
