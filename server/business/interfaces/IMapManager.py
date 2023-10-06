from __future__ import annotations
from abc import ABC, abstractmethod

from business.maps.Map import Map
from typing import TYPE_CHECKING, List

from business.maps.MapName import MapName

if TYPE_CHECKING:
    from business.GameManager import GameManager


class IMapManager(ABC):

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    @abstractmethod
    def get_map(self, map_id: str) -> Map:
        """
        Check if a display client exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_maps_ids(self) -> List[str]:
        """
        Returns all maps id.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_map_names(self) -> List[MapName]:
        """
        Returns all maps names and ids.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_map_data(self, map_id) -> dict:
        """
        Returns all maps id.
        """
        raise NotImplementedError()

    @abstractmethod
    def does_map_exists(self, map_id: str) -> bool:
        """
        Returns all maps id.
        """
        raise NotImplementedError()
