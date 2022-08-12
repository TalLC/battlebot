from common.Singleton import SingletonABCMeta
from business.teams.Team import Team
from business.Common import G_TEAMS


class GameManager(metaclass=SingletonABCMeta):

    @staticmethod
    def does_team_exists(team_id):
        if team_id in G_TEAMS.keys():
            return True
        return False

    @staticmethod
    def get_team(team_id) -> None | Team:
        if team_id in G_TEAMS.keys():
            return G_TEAMS[team_id]
        else:
            return None

    @staticmethod
    def add_team(size, name, color, team_id: str = None) -> str:
        t = Team(size, name, color, team_id)
        return t.id

    def register_bot(self, team_id, bot_name, bot_type) -> str:
        if self.does_team_exists(team_id):
            return self.get_team(team_id).add_bot(bot_name, bot_type)
