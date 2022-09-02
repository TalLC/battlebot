from abc import ABC
from business.gameobjects.entity.bots.Bot import Bot


class IBotManager(ABC):

    def does_bot_exists(self, bot_id):
        """
        Check if a bot exists.
        """
        raise NotImplementedError()

    def get_bot(self, bot_id) -> None | Bot:
        """
        Get a bot by its id.
        """
        raise NotImplementedError()

    def get_bots(self) -> list[Bot]:
        """
        Get all bots.
        """
        raise NotImplementedError()

    def create_bot(self, bot_name, bot_type) -> Bot:
        """
        Add a new bot to an existing team.
        """
        raise NotImplementedError()
