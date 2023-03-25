from business.shapes.ShapesUtils import ShapesUtils
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

    def get_bots(self, connected_only: bool = True, alive_only: bool = True) -> (BotModel,):
        """
        Get all connected bots.
        """
        return tuple(
            bot for bot in self._BOTS.values()
            if (not connected_only or (connected_only and bot.client_connection.is_connected))
            and (not alive_only or (alive_only and bot.is_alive))
        )

    def get_bots_in_radius(self, connected_only: bool = True, alive_only: bool = True,
                           origin: tuple = (0.0, 0.0), radius: int = 1) -> (BotModel,):
        """
        Get all connected bots.
        """
        bots = tuple(
            bot for bot in self._BOTS.values()
            if (not connected_only or (connected_only and bot.client_connection.is_connected))
            and (not alive_only or (alive_only and bot.is_alive))
        )

        # Filtering on radius
        in_range_bots = list()
        for bot in bots:
            if ShapesUtils.get_2d_distance_between(origin, (bot.x, bot.z)) <= radius:
                in_range_bots.append(bot)

        return tuple(in_range_bots)

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

    def reset(self):
        """
        Removes all bots from the game.
        """
        self._BOTS.clear()
