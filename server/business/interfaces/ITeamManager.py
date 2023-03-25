from __future__ import annotations
from abc import ABC, abstractmethod
from business.teams.Team import Team
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.GameManager import GameManager


class ITeamManager(ABC):

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

        # Teams
        self.reload_teams()

    @abstractmethod
    def does_team_exists(self, team_id: str):
        """
        Check if a team exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_team(self, team_id: str) -> None | Team:
        """
        Get a team by its id.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_teams(self) -> [Team]:
        """
        Get all teams.
        """
        raise NotImplementedError()

    def get_bot_team(self, bot_id) -> None | Team:
        """
        Returns the team containing the specified bot.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_team(self, size: int, name: str, color: str, team_id: str = None) -> str:
        """
        Create a new team.
        """
        raise NotImplementedError()

    def bot_count(self, alive_only: bool = False) -> int:
        """
        Get the total number of bots in the teams.
        """
        raise NotImplementedError()

    def reload_teams(self):
        """
        Removes all the teams from the game and reload them.
        """
        raise NotImplementedError()

    def print_teams(self):
        """
        Prints the created teams.
        """
        raise NotImplementedError()
