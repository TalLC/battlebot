import uuid
from abc import ABC
from business.gameobjects.entity.IEntity import IEntity
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.ClientConnection import ClientConnection


class Bot(OrientedGameObject, IEntity, IMoving, IDestructible, ABC):

    @property
    def id(self):
        return self._id

    @property
    def client_connection(self):
        return self._client_connection

    @property
    def role(self):
        return self._ROLE

    def __init__(self, name: str, role: str, health: int, speed: float):
        OrientedGameObject.__init__(self)
        IEntity.__init__(self, name)
        IMoving.__init__(self, speed)
        IDestructible.__init__(self, health, True)
        self._ROLE = role

        # Generate a random id.
        self._id = str(uuid.uuid4())

        # Initialize client communication object
        self._client_connection = ClientConnection(self.id)

    def set_position(self, x: int, z: int, heading: float = 0.0):
        """
        Set the position of the bot.
        Used for spawning the bot on the map.
        """
        self.x = x
        self.z = z
        self.heading = heading

