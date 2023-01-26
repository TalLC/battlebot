from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotStunningStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, stunning: bool):
        super().__init__(bot_id=bot_id, msg_type="stunning_status", stat_value=stunning)
