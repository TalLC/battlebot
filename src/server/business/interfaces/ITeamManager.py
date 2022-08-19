from abc import ABC
from business.teams.Team import Team


class ITeamManager(ABC):

    # TEAMS
    def does_team_exists(self, team_id):
        """
        Check if a team exists.
        """
        raise NotImplementedError()

    def get_team(self, team_id) -> None | Team:
        """
        Get a team by its id.
        """
        raise NotImplementedError()

    def get_teams(self) -> list[Team]:
        """
        Get all teams.
        """
        raise NotImplementedError()

    def add_team(self, size, name, color, team_id: str = None) -> str:
        """
        Add a new team.
        """
        raise NotImplementedError()
