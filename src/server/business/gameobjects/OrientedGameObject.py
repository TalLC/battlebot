from business.gameobjects.GameObject import GameObject
from shapely.geometry import Polygon

"""
    Adding orientation to the GameObject class.
"""


class OrientedGameObject(GameObject):
    def __init__(self, name: str = 'oriented_game_object', ry: float = 0.0, x: float = 0.0, z: float = 0.0,
                 shape: Polygon or None = None):
        super().__init__(name, x, z, shape)
        self.ry = ry
