from consumer.brokers.messages.interfaces.IBotMessage import IBotMessage


class IBotCollisionMessage(IBotMessage):

    def __init__(self, bot_id: str, msg_type: str, object_collided: str):
        data = {
            "collision_with": object_collided
        }
        super().__init__(bot_id=bot_id, msg_type=msg_type, data=data)
