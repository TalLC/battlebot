from common.Singleton import SingletonABCMeta
from business.teams.Team import Team
from business.gameobjects.entity.bots.Bot import Bot


class GameManager(metaclass=SingletonABCMeta):
    _BOTS = dict()
    _TEAMS = dict()

    # TEAMS
    def does_team_exists(self, team_id):
        """
        Check if a team exists.
        """
        if team_id in self._TEAMS.keys():
            return True
        return False

    def get_team(self, team_id) -> None | Team:
        """
        Get a team by its id.
        """
        if team_id in self._TEAMS.keys():
            return self._TEAMS[team_id]
        else:
            return None

    def get_teams(self) -> list[Team]:
        """
        Get all teams.
        """
        return list(self._TEAMS.values())

    def add_team(self, size, name, color, team_id: str = None) -> str:
        """
        Add a new team.
        """
        t = Team(size, name, color, team_id)
        self._TEAMS[t.id] = t
        return t.id

    # BOTS
    def does_bot_exists(self, bot_id):
        """
        Check if a bot exists.
        """
        if bot_id in self._BOTS.keys():
            return True
        return False

    def get_bot(self, bot_id) -> None | Bot:
        """
        Get a bot by its id.
        """
        if bot_id in self._BOTS.keys():
            return self._BOTS[bot_id]
        else:
            return None

    def get_bots(self) -> list[Bot]:
        """
        Get all bots.
        """
        return list(self._BOTS.values())

    def add_bot(self, team_id, bot_name, bot_type) -> None | Bot:
        """
        Add a new bot to an existing team.
        """
        if self.does_team_exists(team_id):
            bot = self.get_team(team_id).add_bot(bot_name, bot_type)
            if bot is not None:
                self._BOTS[bot.id] = bot
            return bot
