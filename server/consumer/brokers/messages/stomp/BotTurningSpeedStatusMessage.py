from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotTurningSpeedStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, turning_speed: float):
        super().__init__(bot_id=bot_id, msg_type="turning_speed_status", stat_value=turning_speed)
