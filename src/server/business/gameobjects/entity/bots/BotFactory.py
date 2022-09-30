from __future__ import annotations
from common.Singleton import SingletonABCMeta
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.Warrior import Warrior
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.BotManager import BotManager


class BotFactory(metaclass=SingletonABCMeta):

    @staticmethod
    def create_bot(bot_manager: BotManager, bot_name: str, bot_type: str) -> BotModel:
        """
        Create a new bot and return the object.
        """
        if bot_type.lower() == "warrior":
            return Warrior(bot_manager, bot_name)
        else:
            return Warrior(bot_manager, bot_name)
