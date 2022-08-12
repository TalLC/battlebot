import random
from abc import ABC
from business.gameobjects.entity.IEntity import IEntity
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.Common import G_BOTS


class Bot(OrientedGameObject, IEntity, IMoving, IDestructible, ABC):

    @property
    def id(self):
        return self._id

    def __init__(self, name: str, health: int = 100, speed: float = 1.0):
        OrientedGameObject.__init__(self)
        IEntity.__init__(self, name)
        IMoving.__init__(self, speed)
        IDestructible.__init__(self, health, True)

        # Generate a random id.
        self._id = self.generate_id()

        # Register the team in the global dictionary.
        self.__register_me()

    def __register_me(self):
        G_BOTS[self.id] = self

    def set_position(self, x: int, z: int, heading: float = 0.0):
        self.x = x
        self.z = z
        self.heading = heading

    @staticmethod
    def generate_id():
        result = ""

        while True:
            for i in range(8):
                result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            if result not in G_BOTS.keys():
                break

        return result
