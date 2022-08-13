from business.gameobjects.entity.bots.Bot import Bot
from business.gameobjects.entity.bots.BotFactory import BotFactory
from common.Generators import Generators


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
    def bots(self):
        return self._bots

    def __init__(self, size: int, name: str, color: str, team_id: str = None):
        self._name = name
        self._color = color
        self._size = size
        self._bots = list()

        # Generate a unique random id if none is provided.
        if team_id != str() and team_id is not None:
            self._id = team_id
        else:
            self._id = Generators().unique_team_id()

    def add_bot(self, bot_name: str, bot_type: str) -> None | Bot:
        """
        Create a new bot and return its id.
        """
        if len(self._bots) < self._size:
            bot = BotFactory().create_bot(bot_name, bot_type)
            self._bots.append(bot)
            return bot
        return None


