from consumer.brokers.messages.interfaces.IMessage import IMessage


class GameStatusMessage(IMessage):

    def __init__(self, bot_id: str, is_started: bool):
        super().__init__(bot_id=bot_id, source='server', msg_type='game_status', data=is_started)

    def json(self) -> dict:
        return {
            'msg_type': self.msg_type,
            'source': self.source,
            'data': {
                'value': self.data
            }
        }
