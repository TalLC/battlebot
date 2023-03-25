from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotMovingStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, moving: bool):
        super().__init__(bot_id=bot_id, msg_type="moving_status", stat_value=moving)
