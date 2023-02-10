from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotWeaponStatusMessage(IBotStatMessage):

    def __init__(self, bot_id: str, can_shoot: bool):
        super().__init__(bot_id=bot_id, msg_type="BotWeaponStatusMessage", stat_value=can_shoot)
