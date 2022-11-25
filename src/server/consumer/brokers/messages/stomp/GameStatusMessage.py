from consumer.brokers.messages.stomp.interfaces.IGameStatusMessage import IGameStatusMessage


class GameStatusMessage(IGameStatusMessage):

    def __init__(self, bot_id: str, is_started: bool):
        super().__init__(bot_id=bot_id, is_started=is_started)
