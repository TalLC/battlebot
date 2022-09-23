import asyncio
import random
import uuid
from abc import ABC
from queue import PriorityQueue
from threading import Thread, Event
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.commands.BotShootCommand import BotShootCommand
from business.gameobjects.entity.bots.commands.BotHurtCommand import BotHurtCommand
from business.gameobjects.entity.bots.commands.BotHealCommand import BotHealCommand
from business.ClientConnection import ClientConnection
from consumer.ConsumerManager import ConsumerManager

from consumer.webservices.messages.websocket.BotMoveMessage import BotMoveMessage
from consumer.webservices.messages.websocket.BotShootMessage import BotShootMessage
from consumer.webservices.messages.websocket.models.Target import Target

from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage


class Bot(OrientedGameObject, IMoving, IDestructible, ABC):

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
        OrientedGameObject.__init__(self, name)
        IMoving.__init__(self, speed)
        IDestructible.__init__(self, health, True)
        self._ROLE = role

        # Generate a random id
        self._id = str(uuid.uuid4())

        # Initialize client communication object
        self._client_connection = ClientConnection(self.id)

        self._commands_queue = PriorityQueue()
        self._thread_event = Event()
        self._thread = Thread(target=self._thread_handle_messages, args=(self._thread_event,)).start()

    def stop_handle_message_thread(self):
        # Set the event to stop the thread
        self._thread_event.set()

    def _thread_handle_messages(self, e: Event):
        while not e.is_set():
            message = self._commands_queue.get(block=True)
            self._route_message(message)

    def _route_message(self, command: IBotCommand):
        if isinstance(command, BotMoveCommand):
            destination = self.move()
            ConsumerManager().websocket.send_message(BotMoveMessage(self.id, destination['x'], destination['z']))
        if isinstance(command, BotShootCommand):
            target = self.shoot(command.value)
            ConsumerManager().websocket.send_message(BotShootMessage(self.id, target))
        if isinstance(command, BotHurtCommand):
            self.hurt(command.value)
            ConsumerManager().stomp.send_message(BotHealthStatusMessage(self.id, self.health))
        if isinstance(command, BotHealCommand):
            self.heal(command.value)
            ConsumerManager().stomp.send_message(BotHealthStatusMessage(self.id, self.health))

    def add_message_to_queue(self, command: IBotCommand):
        self._commands_queue.put(command)

    def set_position(self, x: float, z: float, ry: float = 0.0):
        """
        Set the position of the bot.
        Used for spawning the bot on the map.
        """
        self.x = x
        self.z = z
        self.ry = ry

    def shoot(self, angle: float) -> Target:
        print(f"{self.id} shooting at {angle}")
        r = random.Random()
        x = r.randint(0, 20)
        z = r.randint(0, 20)
        print(f"Impact at {x};{z}")
        target = Target(x, z)
        return target

    def move(self) -> dict:
        r = random.Random()
        x = r.randint(0, 20)
        z = r.randint(0, 20)
        print(f"{self.id} moving at {x};{z}")
        return {'x': x, 'z': z}

