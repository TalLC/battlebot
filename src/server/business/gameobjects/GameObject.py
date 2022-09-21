

class GameObject:
    """
    Base class for every objects on the map.
    """
    def __init__(self, name: str = 'game_object', x: float = 0.0, z: float = 0.0):
        self.name = name
        self.x = x
        self.z = z
