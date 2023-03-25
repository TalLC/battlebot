from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotHealthStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, health: int):
        super().__init__(bot_id=bot_id, msg_type="health_status", stat_value=health)
