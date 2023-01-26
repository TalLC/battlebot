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

    def __init__(self, name: str = 'oriented_game_object', ry: float = 0.0, x: float = 0.0, z: float = 0.0,
                 shape: Polygon or None = None):
        super().__init__(name, x, z, shape)
        self._ry = ry

    def set_position(self, x: float, z: float, ry: float = 0.0):
        """
        Set the position and rotation of the bot.
        """
        self.x = x
        self.z = z
        self.ry = ry
