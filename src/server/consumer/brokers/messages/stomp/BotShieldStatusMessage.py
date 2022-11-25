from consumer.brokers.messages.stomp.interfaces.IShieldMessage import IShieldMessage


class BotShieldStatusMessage(IShieldMessage):

    def __init__(self, bot_id: str, durability_percent: int):
        data = durability_percent
        super().__init__(bot_id=bot_id, msg_type="shield_status", data=data)
