from consumer.brokers.messages.stomp.interfaces.IBotStatMessage import IBotStatMessage


class BotWeaponCooldownMessage(IBotStatMessage):

    def __init__(self, bot_id: str, cooldown_ms: int):
        super().__init__(bot_id=bot_id, msg_type="weapon_cooldown_ms", stat_value=cooldown_ms)
