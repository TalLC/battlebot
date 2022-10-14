from __future__ import annotations
from math import pi, cos, sin
import logging
import random
import uuid
from time import time, sleep
from abc import ABC
from queue import PriorityQueue
from typing import TYPE_CHECKING
from threading import Thread, Event
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.ClientConnection import ClientConnection
from consumer.ConsumerManager import ConsumerManager

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.webservices.messages.websocket.BotMoveMessage import BotMoveMessage
from consumer.webservices.messages.websocket.BotRotateMessage import BotRotateMessage
from consumer.webservices.messages.websocket.models.Target import Target

if TYPE_CHECKING:
    from business.BotManager import BotManager


class BotModel(OrientedGameObject, IMoving, IDestructible, ABC):

    @property
    def id(self) -> str:
        """
        Get bot unique id.
        """
        return self._id

    @property
    def client_connection(self) -> ClientConnection:
        """
        Get bot client connection object describing connection status between the client and the server.
        """
        return self._client_connection

    @property
    def role(self) -> str:
        """
        Name of the role of this bot instance.
        """
        return self._role

    def __init__(self, bot_manager: BotManager, name: str, role: str, health: int, moving_speed: float,
                 turning_speed: float):
        self.bot_manager = bot_manager
        OrientedGameObject.__init__(self, name)
        IMoving.__init__(self, moving_speed, turning_speed)
        IDestructible.__init__(self, health, True)
        self._role = role

        # Generate a random id
        self._id = str(uuid.uuid4())

        # Initialize client communication object
        self._client_connection = ClientConnection(self.id)

        # Commands queue
        self._commands_queue = PriorityQueue()

        # Event to stop all threads at once
        self._thread_event = Event()

        # Thread handling incoming messages
        self._thread_messages = Thread(target=self._thread_handle_commands, args=(self._thread_event,)).start()

        # Thread handling continuous actions as moving and turning
        self._thread_continuous_actions = Thread(
            target=self._thread_handle_continuous_actions,
            args=(self._thread_event,)
        ).start()

    def stop_threads(self):
        """
        Stop all threads for this bot.
        """
        # Set the event to stop the thread
        self._thread_event.set()

    def _thread_handle_commands(self, e: Event):
        """
        Execute commands from the queue.
        """
        while not e.is_set():
            command = self._commands_queue.get(block=True)
            logging.debug(f"BOT {self.id} - Incoming command: {command}")

            if isinstance(command, IBotCommand):
                command.execute(self)

    def _thread_handle_continuous_actions(self, e: Event):
        """
        Handling continuous actions such as moving and turning.
        This thread use the elapsed time from last movement to compute the increment to add
        to an action (ie: move, turn, ...).
        """
        # Waiting interval between all increments
        loop_wait_ms = 10

        while not e.is_set():

            # Action: Move
            if self.is_moving:

                # If this is the first movement of this type, here is our starting point
                # We will start to actually move next loop
                if self.last_move_timestamp == 0.0:
                    self.last_move_timestamp = time()
                else:
                    # A loop has elapsed, we move the bot on an equivalent distance

                    # Get the timestamp delta between this loop and the previous one
                    current_ts = time()
                    interval_ts = current_ts - self.last_move_timestamp

                    # traveled_distance = moving speed * movement duration
                    traveled_distance = self.get_distance_from_time_and_speed(self.moving_speed, interval_ts)

                    # Actually move the bot on the map
                    self.move(traveled_distance)

                    # Reset timestamp for next loop
                    self.last_move_timestamp = time()

            # Action: Turn
            if self.is_turning:
                # If this is the first movement of this type, here is our starting point
                # We will start to actually move next loop
                if self.last_turn_timestamp == 0.0:
                    self.last_turn_timestamp = time()
                else:
                    # A loop has elapsed, we turn equivalent radians

                    # Get the timestamp delta between this loop and the previous one
                    current_ts = time()
                    interval_ts = current_ts - self.last_turn_timestamp

                    # radians = turning speed * movement duration
                    radians = self.get_turn_from_time_and_speed(self.turning_speed, interval_ts)

                    # Actually move the bot on the map
                    self.turn(radians)

                    # Reset timestamp for next loop
                    self.last_turn_timestamp = time()

            # Waiting before next loop
            sleep(loop_wait_ms / 1000)

    def add_command_to_queue(self, command: IBotCommand):
        """
        Add a command message to the bot queue.
        """
        self._commands_queue.put(command)

    def set_position(self, x: float, z: float, ry: float = 0.0):
        """
        Set the position and rotation of the bot.
        """
        self.x = x
        self.z = z
        self.ry = ry

    def shoot(self, angle: float) -> Target:
        # WIP
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
        """
        Turn the bot on Y axis of the specified amount of radians.
        """
        max_rotation = pi * 2
        min_rotation = 0.0

        # Using the direction to decide if we add or subtract radians
        if self.turn_direction == 'left':
            self.ry -= radians
        elif self.turn_direction == 'right':
            self.ry += radians

        # We keep the value between its max and min
        if self.ry < min_rotation:
            self.ry += max_rotation
        elif self.ry > max_rotation:
            self.ry -= max_rotation

        # Sending new rotation over websocket
        ConsumerManager().websocket.send_message(BotRotateMessage(self.id, self.ry))

    def move(self, distance: float):
        """
        Move the bot forward on X and Z axis using its current rotation.
        """

        # Calculating new coordinates
        new_x = cos(self.ry) * distance
        new_z = sin(self.ry) * distance

        # Moving the bot on the map
        self.set_position(self.x + new_x, self.z + new_z, self.ry)

        # Sending new position over websocket
        ConsumerManager().websocket.send_message(BotMoveMessage(self.id, self.x, self.z))
