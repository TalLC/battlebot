import uuid

from shapely.geometry.base import BaseGeometry


class GameObject:
    """
    Base class for every objects on the map.
    """

    @property
    def id(self) -> str:
        """
        Unique identifier.
        """
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def coordinates(self) -> tuple[float, float]:
        return self.x, self.z

    @property
    def shape(self) -> BaseGeometry:
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value

    def __init__(self, name: str = 'game_object', x: float = 0.0, z: float = 0.0, shape: BaseGeometry or None = None):
        self._id = str(uuid.uuid4())
        self._name = name
        self.x = x
        self.z = z
        self._shape = shape
