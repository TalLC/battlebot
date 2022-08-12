import random
from business.gameobjects.entity.bots.BotFactory import BotFactory
from business.Common import G_TEAMS


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

        # Generate a random id if none is provided.
        if team_id != str() and team_id is not None:
            self._id = team_id
        else:
            self._id = self.generate_id()

        # Register the team in the global dictionary.
        self.__register_me()

    def __register_me(self):
        G_TEAMS[self.id] = self

    def add_bot(self, bot_name: str, bot_type: str) -> str:
        """
        Create a new bot and return its id.
        """
        if len(self._bots) < self._size:
            bot = BotFactory().create_bot(bot_name, bot_type)
            self._bots.append(bot)
            return bot.id
        return str()

    @staticmethod
    def generate_id():
        result = ""

        while True:
            for i in range(8):
                result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            if result not in G_TEAMS.keys():
                break

        return result
