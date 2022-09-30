from common.Singleton import SingletonABCMeta
from business.interfaces.IGameManager import IGameManager
from business.TeamManager import TeamManager
from business.BotManager import BotManager
from business.DisplayManager import DisplayManager
from business.Map import Map


class GameManager(IGameManager, metaclass=SingletonABCMeta):

    @property
    def is_started(self) -> bool:
        return self._is_started

    def __init__(self):
        self._is_started = False
        self.team_manager = TeamManager(self)
        self.bot_manager = BotManager(self)
        self.display_manager = DisplayManager(self)
        self.map = Map(self)

    def start_game(self):
        self._is_started = True
