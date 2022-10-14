from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotTurningStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, turning: str):
        super().__init__(bot_id=bot_id, msg_type="turning_status", stat_value=turning)
