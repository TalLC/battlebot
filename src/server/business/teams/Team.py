from __future__ import annotations
import uuid
from business.gameobjects.entity.bots.models.BotModel import BotModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.TeamManager import TeamManager


class Team:

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> str:
        return self._color

    @property
    def size(self) -> int:
        return self._size

    @property
    def bots(self) -> dict[str, BotModel]:
        return self._bots

    @property
    def alive_bots_count(self) -> int:
        """
        Get the number of bot alive in the team.
        """
        return len([bot for bot in self.bots.values() if bot.is_alive])

    @property
    def is_alive(self) -> bool:
        """
        Returns true if at least one bot is still alive in the team.
        """
        return self.alive_bots_count > 0

    def __init__(self, team_manager: TeamManager, size: int, name: str, color: str, team_id: str = None):
        self.team_manager = team_manager
        self._name = name
        self._color = color
        self._size = size
        self._bots: dict[str, BotModel] = dict()

        # Generate a unique random id if none is provided.
        if team_id != str() and team_id is not None:
            self._id = team_id
        else:
            self._id = str(uuid.uuid4())

    def __str__(self):
        return f"{self.name} ({self.id}) - " \
               f"COLOR: {self.color}, " \
               f"SIZE: {self.size}"

    def add_bot(self, bot: BotModel) -> bool:
        """
        Add an existing bot to the team.
        """
        if len(self._bots) < self._size:
            self._bots[bot.id] = bot
            return True
        return False

    def get_bot(self, bot_id) -> None | BotModel:
        """
        Get a bot by its id.
        """
        if bot_id in self.bots.keys():
            return self.bots[bot_id]
        else:
            return None
