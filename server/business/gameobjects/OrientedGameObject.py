import math
from math import pi
from business.gameobjects.GameObject import GameObject
from shapely.geometry import Polygon

"""
    Adding orientation to the GameObject class.
"""


class OrientedGameObject(GameObject):

    @property
    def ry(self) -> float:
        """
        The value is contained between 0.0 and 2pi.
        """
        return self._ry

    @ry.setter
    def ry(self, value):
        """
        Sets the value to a value between 0.0 and 2pi.
        """
        self._ry = value % (2*pi)

    @property
    def forward_vector(self) -> tuple:
        return math.sin(self.ry), math.cos(self.ry)

    @property
    def backward_vector(self) -> tuple:
        return math.sin(-1 * self.ry), math.cos(-1 * self.ry)

    def __init__(self, name: str = 'oriented_game_object', friendly_name: str = 'Oriented game object',
                 object_type: str = 'object', ry: float = 0.0, x: float = 0.0, z: float = 0.0,
                 shape: Polygon or None = None):
        super().__init__(name=name, friendly_name=friendly_name, object_type=object_type, x=x, z=z, shape=shape)
        self._ry = ry

    def set_position(self, x: float, z: float, ry: float = 0.0):
        """
        Set the position and rotation of the bot.
        """
        self.x = x
        self.z = z
        self.ry = ry
