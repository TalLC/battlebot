from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject


class TileObject(OrientedGameObject, IDestructible):

    def __init__(self, x: int, z: int, heading: float = 0.0, health: int = 0, has_collision: bool = False):
        OrientedGameObject.__init__(self, heading, x, z)
        IDestructible.__init__(self, health)

        self._HEALTH_MAX = health
        self._HEALTH = self._HEALTH_MAX
        self._HAS_COLLISION = has_collision
