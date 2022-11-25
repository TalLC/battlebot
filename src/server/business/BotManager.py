from business.interfaces.IBotManager import IBotManager
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.BotFactory import BotFactory


class BotManager(IBotManager):

    _BOTS: dict[str, BotModel] = dict()

    def does_bot_exists(self, bot_id):
        """
        Check if a bot exists.
        """
        if bot_id in self._BOTS.keys():
            return True
        return False

    def get_bot(self, bot_id) -> None | BotModel:
        """
        Get a bot by its id.
        """
        if bot_id in self._BOTS.keys():
            return self._BOTS[bot_id]
        else:
            return None

    def get_bots(self, connected_only: bool = True) -> (BotModel,):
        """
        Get all connected bots.
        """
        bots = tuple(self._BOTS.values())

        if connected_only:
            bots = (bot for bot in self._BOTS.values() if bot.client_connection.is_connected is connected_only)

        return tuple(bots)

    def create_bot(self, bot_name, bot_type) -> BotModel:
        """
        Create a new bot.
        """
        bot = BotFactory().create_bot(self, bot_name, bot_type)
        self._BOTS[bot.id] = bot
        return bot

    def get_bots_count(self, connected_only: bool = True):
        """
        Return the total amount of connected bots.
        """
        return len(self.get_bots(connected_only))
