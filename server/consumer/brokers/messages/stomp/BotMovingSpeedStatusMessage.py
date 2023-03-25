from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotMovingSpeedStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, moving_speed: float):
        super().__init__(bot_id=bot_id, msg_type="moving_speed_status", stat_value=moving_speed)
