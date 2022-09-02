from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotDamageReceivedMessage(IBotStatMessage):
    _MESSAGE_TYPE = "damage_received"

    def __init__(self, bot_id: str, damages: int):
        super().__init__(bot_id, self._MESSAGE_TYPE, damages)
