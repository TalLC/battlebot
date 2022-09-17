from business.interfaces.ITeamManager import ITeamManager
from business.teams.Team import Team


class TeamManager(ITeamManager):
    _TEAMS = dict()

    def does_team_exists(self, team_id: str):
        """
        Check if a team exists.
        """
        if team_id in self._TEAMS.keys():
            return True
        return False

    def get_team(self, team_id: str) -> None | Team:
        """
        Get a team by its id.
        """
        if team_id in self._TEAMS.keys():
            return self._TEAMS[team_id]
        else:
            return None

    def get_teams(self) -> [Team]:
        """
        Get all teams.
        """
        return list(self._TEAMS.values())

    def create_team(self, size: int, name: str, color: str, team_id: str = None) -> str:
        """
        Create a new team.
        """
        t = Team(size, name, color, team_id)
        self._TEAMS[t.id] = t
        return t.id
