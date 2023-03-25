import logging
from common.config import CONFIG_TEAMS
from business.interfaces.ITeamManager import ITeamManager
from business.teams.Team import Team


class TeamManager(ITeamManager):
    _TEAMS: dict[str, Team] = dict()

    def does_team_exists(self, team_id: str):
        if team_id in self._TEAMS.keys():
            return True
        return False

    def get_team(self, team_id: str) -> None | Team:
        if team_id in self._TEAMS.keys():
            return self._TEAMS[team_id]
        else:
            return None

    def get_teams(self, still_alive_only: bool = False) -> (Team,):
        if still_alive_only:
            return tuple([team for team in self._TEAMS.values() if team.is_alive])
        else:
            return tuple(self._TEAMS.values())

    def get_bot_team(self, bot_id) -> None | Team:
        for team in self._TEAMS.values():
            if team.get_bot(bot_id) is not None:
                return team

        return None

    def create_team(self, size: int, name: str, color: str, team_id: str = None) -> str:
        t = Team(self, size, name, color, team_id)
        self._TEAMS[t.id] = t
        return t.id

    def bot_count(self, alive_only: bool = False) -> int:
        bot_count = 0
        for team in self.get_teams():
            bot_count += team.bot_count(alive_only=alive_only)
        return bot_count

    def reload_teams(self):
        self._TEAMS.clear()

        for team in CONFIG_TEAMS:
            self.create_team(team.size, team.name, team.color, team.id)

        logging.info("[TEAMMANAGER] Created teams:")
        self.print_teams()

    def print_teams(self):
        for team in self.get_teams():
            logging.info(team)
