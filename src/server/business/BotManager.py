import logging

from business.interfaces.IBotManager import IBotManager
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.BotFactory import BotFactory


class BotManager(IBotManager):

    _BOTS = dict()

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

    def get_bots(self) -> list[BotModel]:
        """
        Get all bots.
        """
        return list(self._BOTS.values())

    def create_bot(self, bot_name, bot_type) -> BotModel:
        """
        Create a new bot.
        """
        bot = BotFactory().create_bot(bot_name, bot_type)
        self._BOTS[bot.id] = bot
        logging.info(self._BOTS)
        return bot
