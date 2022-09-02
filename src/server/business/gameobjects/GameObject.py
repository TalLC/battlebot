
"""
    Base class for every objects on the map.
"""


class GameObject:

    def __init__(self, name: str = 'game_object', x: int = 0, z: int = 0):
        self.name = name
        self.x = x
        self.z = z
