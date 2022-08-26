from abc import abstractmethod, ABC


class IAction(ABC):

    def __init__(self, bot_id: str):
        self.bot_id = bot_id

    @abstractmethod
    def get_message(self) -> dict:
        raise NotImplementedError()
