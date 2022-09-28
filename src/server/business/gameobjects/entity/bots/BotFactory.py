from common.Singleton import SingletonABCMeta
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.Warrior import Warrior


class BotFactory(metaclass=SingletonABCMeta):

    @staticmethod
    def create_bot(bot_name: str, bot_type: str) -> BotModel:
        """
        Create a new bot and return the object.
        """
        if bot_type.lower() == "warrior":
            return Warrior(bot_name)
        else:
            return Warrior(bot_name)
