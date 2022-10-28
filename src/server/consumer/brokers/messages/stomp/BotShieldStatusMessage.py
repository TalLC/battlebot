from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotShieldStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, durability_percent: int):
        super().__init__(bot_id=bot_id, msg_type="shield_status", stat_value=durability_percent)
