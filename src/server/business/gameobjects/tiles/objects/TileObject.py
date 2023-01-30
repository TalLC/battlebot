from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from shapely.geometry import Polygon

from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from consumer.ConsumerManager import ConsumerManager
from consumer.webservices.messages.websocket.GameObjectDestroyMessage import GameObjectDestroyMessage

if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile


class TileObject(OrientedGameObject, IDestructible, ABC):

    @property
    def tile(self) -> Tile:
        return self._tile

    @property
    @abstractmethod
    def shape_name(self) -> str:
        return str()

    @property
    @abstractmethod
    def shape_size(self) -> float:
        return 0.0

    def __init__(self, parent_tile: Tile, name: str, x: float, z: float, heading: float = 0.0, health: int = 0,
                 has_collision: bool = False, shape: Polygon or None = None):
        OrientedGameObject.__init__(self, name=name, ry=heading, x=x, z=z, shape=shape)
        IDestructible.__init__(self, health, has_collision)

        self._HEALTH_MAX = health
        self._HEALTH = self._HEALTH_MAX
        self._HAS_COLLISION = has_collision
        self._tile = parent_tile

    def __str__(self):
        return f"{self.name} ({self.id})"

    def __eq__(self, other):
        return self.name == other.name and self.x == other.x and self.z == other.z

    def _on_death(self) -> None:
        # Removing object on the display side
        self.tile.set_tile_object("air")
        ConsumerManager().websocket.send_message(GameObjectDestroyMessage(self.id))
