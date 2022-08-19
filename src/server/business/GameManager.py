from common.Singleton import SingletonABCMeta
from business.interfaces.IGameManager import IGameManager
from business.TeamManager import TeamManager
from business.BotManager import BotManager


class GameManager(IGameManager, metaclass=SingletonABCMeta):

    def __init__(self):
        self.team_manager = TeamManager()
        self.bot_manager = BotManager()
