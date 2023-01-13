import uuid
from typing import Tuple

from shapely.geometry import Polygon


class GameObject:
    """
    Base class for every objects on the map.
    """

    @property
    def id(self):
        """
        Unique identifier.
        """
        return self._id

    @property
    def coordinates(self) -> Tuple[float, float]:
        return self.x, self.z

    def __init__(self, name: str = 'game_object', x: float = 0.0, z: float = 0.0, shape: Polygon or None = None):
        self._id = str(uuid.uuid4())
        self.name = name
        self.x = x
        self.z = z
        self.shape = shape
