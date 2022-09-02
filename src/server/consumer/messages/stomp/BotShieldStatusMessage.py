from consumer.messages.stomp.interfaces.IShieldMessage import IShieldMessage


class BotScannerDetectionMessage(IShieldMessage):
    _MESSAGE_TYPE = "shield_status"

    def __init__(self, bot_id: str, durability_percent: int):
        data = durability_percent
        super().__init__(bot_id, self._MESSAGE_TYPE, data)
