from consumer.actions.interfaces.IAction import IAction


class ActionSendStompId(IAction):

    def __init__(self, bot_id: str, stomp_id: str):
        self.stomp_id = stomp_id
        super().__init__(bot_id)

    def get_message(self) -> dict:
        return {"stomp_id": self.stomp_id}
