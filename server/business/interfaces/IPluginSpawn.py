from abc import ABC, abstractmethod


class IPluginSpawn(ABC):

    @property
    def map(self):
        return self._map
    def __init__(self, map):
        self._map = map
        pass

    @abstractmethod
    def process(self, team_id) -> tuple:
        """
        Method of spawn.
        """
        raise NotImplementedError()

    @abstractmethod
    def required(self) -> bool:
        """
        Verification for usage method of spawn.
        """
        raise NotImplementedError()