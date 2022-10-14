from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotDamageReceivedMessage(IBotStatMessage):

    def __init__(self, bot_id: str, damages: int):
        super().__init__(bot_id=bot_id, msg_type="damage_received", stat_value=damages)
