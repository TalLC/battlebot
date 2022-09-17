from abc import ABC, abstractmethod
from business.teams.Team import Team


class ITeamManager(ABC):

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

    @abstractmethod
    def create_team(self, size: int, name: str, color: str, team_id: str = None) -> str:
        """
        Create a new team.
        """
        raise NotImplementedError()
