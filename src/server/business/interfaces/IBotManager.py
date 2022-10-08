from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.models.BotModel import BotModel

if TYPE_CHECKING:
    from business.GameManager import GameManager


class IBotManager(ABC):

    def __init__(self, game_manager: GameManager):
        self._game_manager = game_manager

    def does_bot_exists(self, bot_id):
        """
        Check if a bot exists.
        """
        raise NotImplementedError()

    def get_bot(self, bot_id) -> None | BotModel:
        """
        Get a bot by its id.
        """
        raise NotImplementedError()

    def get_bots(self) -> [BotModel]:
        """
        Get all bots.
        """
        raise NotImplementedError()

    def create_bot(self, bot_name, bot_type) -> BotModel:
        """
        Add a new bot to an existing team.
        """
        raise NotImplementedError()

    def get_bots_count(self, connected_only: bool = True):
        """
        Return the total amount of connected bots.
        """
        raise NotImplementedError()
