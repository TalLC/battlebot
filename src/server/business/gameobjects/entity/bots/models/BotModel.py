import asyncio
import math
from time import time, sleep
import logging
import random
import uuid
from abc import ABC
from queue import PriorityQueue
from threading import Thread, Event
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.ClientConnection import ClientConnection
from consumer.ConsumerManager import ConsumerManager

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.commands.BotTurnCommand import BotTurnCommand
from business.gameobjects.entity.bots.commands.BotShootCommand import BotShootCommand
from business.gameobjects.entity.bots.commands.BotHurtCommand import BotHurtCommand
from business.gameobjects.entity.bots.commands.BotHealCommand import BotHealCommand

from consumer.webservices.messages.websocket.BotMoveMessage import BotMoveMessage
from consumer.webservices.messages.websocket.BotRotateMessage import BotRotateMessage
from consumer.webservices.messages.websocket.BotShootMessage import BotShootMessage
from consumer.webservices.messages.websocket.models.Target import Target

from consumer.brokers.messages.stomp.BotMovingStatusMessage import BotMovingStatusMessage
from consumer.brokers.messages.stomp.BotTurningStatusMessage import BotTurningStatusMessage
from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage


class BotModel(OrientedGameObject, IMoving, IDestructible, ABC):

    @property
    def id(self):
        return self._id

    @property
    def client_connection(self):
        return self._client_connection

    @property
    def role(self):
        return self._role

    def __init__(self, name: str, role: str, health: int, moving_speed: float, turning_speed: float):
        OrientedGameObject.__init__(self, name)
        IMoving.__init__(self, moving_speed, turning_speed)
        IDestructible.__init__(self, health, True)
        self._role = role

        # Generate a random id
        self._id = str(uuid.uuid4())

        # Initialize client communication object
        self._client_connection = ClientConnection(self.id)

        self._commands_queue = PriorityQueue()
        self._thread_event = Event()
        self._thread_messages = Thread(target=self._thread_handle_messages, args=(self._thread_event,)).start()
        self._thread_actions = Thread(target=self._thread_continuous_actions, args=(self._thread_event,)).start()

    def stop_handle_message_thread(self):
        # Set the event to stop the thread
        self._thread_event.set()

    def _thread_handle_messages(self, e: Event):
        while not e.is_set():
            message = self._commands_queue.get(block=True)
            self._route_message(message)

    def _thread_continuous_actions(self, e: Event):
        loop_wait_ms = 100

        while not e.is_set():
            if self.is_moving:

                # If it is the first move we make, we won't move
                if self.last_move_timestamp == 0.0:
                    self.last_move_timestamp = time()
                else:
                    # A loop is elapsed, we move an equivalent distance
                    current_ts = time()
                    interval_ts = current_ts - self.last_move_timestamp

                    traveled_distance = self.get_distance_from_time_and_speed(self.moving_speed, interval_ts)

                    self.move(traveled_distance)
                    self.last_move_timestamp = time()
            if self.is_turning:
                # If it is the first turn we make, we won't turn
                if self.last_turn_timestamp == 0.0:
                    self.last_turn_timestamp = time()
                else:
                    # A loop is elapsed, we turn equivalent radians
                    current_ts = time()
                    interval_ts = current_ts - self.last_turn_timestamp

                    radians = self.get_turn_from_time_and_speed(self.moving_speed, interval_ts)
                    self.turn(radians)
                    self.last_turn_timestamp = time()

            sleep(loop_wait_ms / 1000)

    def _route_message(self, command: IBotCommand):
        logging.debug(f"BOT {self.id} - Incoming message: {command}")
        if isinstance(command, BotMoveCommand):
            if command.value == "stop":
                self.set_moving(False)
            else:
                self.set_moving(True)
            ConsumerManager().stomp.send_message(BotMovingStatusMessage(self.id, self.is_moving))
        if isinstance(command, BotTurnCommand):
            if command.value == "stop":
                self.set_turning(False)
            else:
                self.set_turning(True, command.value)
            ConsumerManager().stomp.send_message(BotTurningStatusMessage(self.id, command.value))
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
        from business.GameManager import GameManager
        game_map = GameManager().map
        r = random.Random()
        x = r.randint(0, game_map.width - 1)
        z = r.randint(0, game_map.height - 1)
        print(f"Impact at {x};{z}")
        target = Target(x, z)
        return target

    def turn(self, radians: float):

        max_rotation = math.pi * 2
        min_rotation = 0.0

        if self.turn_direction == 'left':
            self.ry -= radians
        elif self.turn_direction == 'right':
            self.ry += radians

        if self.ry < min_rotation:
            self.ry += max_rotation
        elif self.ry > max_rotation:
            self.ry -= max_rotation

        ConsumerManager().websocket.send_message(BotRotateMessage(self.id, self.ry))

    def move(self, distance: float):

        new_x = math.cos(self.ry) * distance
        new_z = math.sin(self.ry) * distance

        self.set_position(self.x + new_x, self.z + new_z, self.ry)

        ConsumerManager().websocket.send_message(BotMoveMessage(self.id, self.x, self.z))


        # from business.GameManager import GameManager
        # game_map = GameManager().map
        # r = random.Random()
        # x = r.randint(0, game_map.width - 1)
        # z = r.randint(0, game_map.height - 1)
        # print(f"{self.id} moving at {x};{z}")
        # return {'x': x, 'z': z}

