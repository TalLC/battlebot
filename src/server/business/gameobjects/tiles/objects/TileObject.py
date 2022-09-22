from abc import ABC
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject


class TileObject(OrientedGameObject, IDestructible, ABC):

    def __init__(self, name: str, x: int, z: int, heading: float = 0.0, health: int = 0, has_collision: bool = False):
        OrientedGameObject.__init__(self, name, heading, x, z)
        IDestructible.__init__(self, health)

        self._HEALTH_MAX = health
        self._HEALTH = self._HEALTH_MAX
        self._HAS_COLLISION = has_collision

    def __str__(self):
        return f"{self.name}"
