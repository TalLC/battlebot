from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from business.maps.Map import Map


class IPluginSpawn(ABC):

    @property
    def game_map(self):
        return self._game_map

    def __init__(self, game_map: Map):
        self._game_map = game_map

    @abstractmethod
    def process(self, team_id) -> Tuple[float, float, float]:
        """
        Return x, ry and z coordinates.
        """
        raise NotImplementedError()

    @abstractmethod
    def required(self) -> bool:
        """
        Check prerequisites for spawn method.
        """
        raise NotImplementedError()
