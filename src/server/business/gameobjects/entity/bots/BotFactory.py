from common.Singleton import SingletonABCMeta
from business.gameobjects.entity.bots.Bot import Bot
from business.gameobjects.entity.bots.Warrior import Warrior


class BotFactory(metaclass=SingletonABCMeta):

    @staticmethod
    def create_bot(bot_name: str, bot_type: str) -> Bot:
        """
        Create a new bot and return the object.
        """
        if bot_type.lower() == "warrior":
            return Warrior(bot_name)
        else:
            return Warrior(bot_name)
