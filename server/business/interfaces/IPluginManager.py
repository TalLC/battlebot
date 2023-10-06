from __future__ import annotations
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from business.maps.Map import Map
    from business.interfaces.IPluginSpawn import IPluginSpawn


class IPluginManager(ABC):

    @abstractmethod
    def get_plugin_spawn_for_map(self, game_map: Map) -> IPluginSpawn:
        """
        Give the available spawn plugins for a specific map
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def __get_available_spawn_plugins() -> List[str]:
        """
        Return all plugins declared in game config
        """
        raise NotImplementedError()
