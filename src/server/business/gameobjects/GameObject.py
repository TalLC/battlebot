
"""
    Base class for every objects on the map.
"""


class GameObject:

    def __init__(self, x: int = 0, z: int = 0):
        self.x = x
        self.z = z
