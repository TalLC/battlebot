from business.gameobjects.GameObject import GameObject

"""
    Adding orientation to the GameObject class.
"""


class OrientedGameObject(GameObject):
    def __init__(self, name: str = 'oriented_game_object', ry: float = 0.0, x: float = 0.0, z: float = 0.0):
        super().__init__(name, x, z)
        self.ry = ry
