from business.gameobjects.GameObject import GameObject

"""
    Adding orientation to the GameObject class.
"""


class OrientedGameObject(GameObject):
    def __init__(self, ry: float = 0.0, x: int = 0, z: int = 0):
        super().__init__(x, z)
        self.heading = ry
