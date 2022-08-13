import random
from common.Singleton import SingletonABCMeta


class Generators(metaclass=SingletonABCMeta):
    _BOTS_ID = list()
    _TEAMS_ID = list()

    @staticmethod
    def random_id() -> str:
        result = ""

        for i in range(8):
            result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

        return result

    def unique_bot_id(self) -> str:
        result = ""

        while True:
            for i in range(8):
                result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            if result not in self._BOTS_ID:
                break

        return result

    def unique_team_id(self) -> str:
        result = ""

        while True:
            for i in range(8):
                result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            if result not in self._TEAMS_ID:
                break

        return result
