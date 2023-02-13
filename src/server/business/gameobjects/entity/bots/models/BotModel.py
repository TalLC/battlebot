from __future__ import annotations

import math
from random import Random
from math import pi
import logging
from time import time, sleep
from datetime import timedelta
from abc import ABC, abstractmethod
from queue import PriorityQueue
from typing import TYPE_CHECKING
from threading import Thread, Event
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.ClientConnection import ClientConnection
from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.handlers.CollisionHandler import CollisionHandler
from business.shapes.ShapeFactory import Shape
from business.gameobjects.entity.bots.commands.BotTurnCommand import BotTurnCommand
from business.gameobjects.entity.bots.equipments.Equipment import Equipment
from business.shapes.ShapesUtils import ShapesUtils, ShapeFactory
from consumer.ConsumerManager import ConsumerManager

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage
from consumer.webservices.messages.websocket.BotMoveMessage import BotMoveMessage
from consumer.webservices.messages.websocket.BotRotateMessage import BotRotateMessage
from consumer.webservices.messages.websocket.GameObjectHurtMessage import GameObjectHurtMessage
from consumer.webservices.messages.websocket.BotDeathMessage import BotDeathMessage
from consumer.webservices.messages.websocket.models.Target import Target

if TYPE_CHECKING:
    from business.gameobjects.GameObject import GameObject
    from business.BotManager import BotManager
    from shapely.geometry.base import BaseGeometry
    from business.TeamManager import Team


class BotModel(OrientedGameObject, IMoving, IDestructible, ABC):

    @property
    def id(self) -> str:
        """
        Get bot unique id.
        """
        return self._id

    @property
    def team(self) -> Team:
        """
        Get the bots team.
        """
        return self.bot_manager.game_manager.team_manager.get_bot_team(self.id)

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

    @property
    def equipment(self) -> Equipment:
        """
        Get the equipment.
        """
        return self._equipment

    @property
    def shape(self) -> BaseGeometry:
        return ShapeFactory().create_shape(
            Shape.CIRCLE, o=(self.x, self.z), radius=self.shape_size, resolution=3
        )

    @property
    def shape_name(self) -> str:
        return self._shape_name

    @property
    def shape_size(self) -> float:
        return self._shape_size

    @property
    def ry_deg(self):
        return self.ry * (180 / pi)

    @property
    def event_stop_threads(self):
        return self._event_stop_threads

    @property
    def collision_handler(self) -> CollisionHandler:
        """
        3D model to use.
        """
        return self._collision_handler

    @abstractmethod
    def model_name(self) -> str:
        """
        3D model to use.
        """
        raise NotImplementedError

    def __init__(self, bot_manager: BotManager, name: str, role: str, health: int, moving_speed: float,
                 turning_speed: float, shape_name: str, shape_size: float):
        self.bot_manager = bot_manager

        # Role name
        self._role = role

        # The equipment is defined by the bot role
        self._equipment: Equipment = Equipment()

        # Parents initializations
        OrientedGameObject.__init__(self, name=name, object_type="bot")
        IMoving.__init__(self, entity=self, moving_speed=moving_speed, turning_speed=turning_speed)
        IDestructible.__init__(self, health, True)

        # Collision
        self._shape_name = shape_name
        self._shape_size = shape_size
        self._collision_handler = CollisionHandler(self)

        # Random starting point
        self.x, self.z = bot_manager.game_manager.map.get_random_spawn_coordinates()
        # Random starting rotation
        self.ry = Random().randint(0, math.floor(2 * pi * 100)) / 100

        # Initialize client communication object
        self._client_connection = ClientConnection(self.id)

        # Commands queue
        self._commands_queue = PriorityQueue()

        # Event to stop all threads at once
        self._event_stop_threads = Event()

        # Thread handling incoming messages
        self._thread_messages = Thread(
            target=self._thread_handle_commands,
            args=(self._event_stop_threads,)
        ).start()

        # Thread handling continuous actions as moving and turning
        self._thread_continuous_actions = Thread(
            target=self._thread_handle_continuous_actions,
            args=(self._event_stop_threads,)
        ).start()

    def stop(self):
        """
        Stops properly all bot activities.
        To use when the game is over or when the bot died.
        """
        Thread(target=self._thread_stop_bot).start()

    def stop_threads(self):
        """
        Stop all threads for this bot.
        """
        # Set the event to stop the threads
        self._event_stop_threads.set()

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

                # If this is the first movement of this type, we set the last move timestamp to one loop behind in
                # order to let the bot move right now instead of waiting the next loop
                if self.last_move_timestamp == 0.0:
                    self.last_move_timestamp = time() - timedelta(milliseconds=loop_wait_ms).total_seconds()

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
                # If this is the first movement of this type, we set the last move timestamp to one loop behind in
                # order to let the bot move right now instead of waiting the next loop
                if self.last_turn_timestamp == 0.0:
                    self.last_turn_timestamp = time() - timedelta(milliseconds=loop_wait_ms).total_seconds()

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

    def _thread_stop_bot(self):
        # Stopping scanner
        logging.debug(f"[BOT {self.name}] Stopping scanner")
        self.equipment.scanner.switch()

        # Stopping the bot
        logging.debug(f"[BOT {self.name}] Stopping movements")
        self.add_command_to_queue(BotMoveCommand(priority=0, value='stop'))
        self.add_command_to_queue(BotTurnCommand(priority=0, value="stop"))

        # Waiting for bot to be stopped
        while self.is_turning or self.is_moving:
            sleep(0.01)
        logging.debug(f"[BOT {self.name}] Is stopped")

        # Killing threads
        self.stop_threads()
        logging.debug(f"[BOT {self.name}] Threads stopped")

    def add_command_to_queue(self, command: IBotCommand):
        """
        Add a command message to the bot queue.
        """
        self._commands_queue.put(command)

    def shoot(self, angle: float) -> Target:
        """
        Called by Rest when the bot is ordered to shoot.
        Return the target that was hit (can be a GameObject or coordinates if nothing was hit).
        """
        # Clamping the angle value to its limits according to the scanner capabilities
        shoot_angle = sorted((self.equipment.scanner.fov / -2, angle, self.equipment.scanner.fov / 2))[1]

        # Maximum fire distance depends on the weapon capabilities
        shoot_max_distance = self.equipment.weapon.reach_distance

        # Maximum end coordinate of the shoot
        shoot_end_x, shoot_end_z = ShapesUtils.get_coordinates_at_distance(
            (self.x, self.z), shoot_max_distance, self.ry + math.radians(shoot_angle)
        )

        # Gathering map objects
        map_objects = self.bot_manager.game_manager.get_map_objects(
            bots=True, tiles=False, collision_only=True, radius=shoot_max_distance, origin=self.coordinates
        )
        # Avoid shooting in our foot
        map_objects.remove(self)

        # Test which objects can be shot
        closest_object: GameObject | None = None
        touched_objects = ShapesUtils.cast_ray_on_objects((self.x, self.z), (shoot_end_x, shoot_end_z), map_objects)
        if len(touched_objects):
            sorted_objects = sorted(
                touched_objects,
                key=lambda obj: ShapesUtils.get_2d_distance_between((self.x, self.z), obj.coordinates)
            )
            closest_object = sorted_objects[0]

        # If an object was shot, we return it
        if closest_object is not None:
            # We have one object that was shot
            return Target(id=closest_object.id)
        else:
            # No object was harmed
            return Target(x=shoot_end_x, z=shoot_end_z)

    def turn(self, radians: float):
        """
        Turn the bot on Y axis of the specified amount of radians.
        """
        # Using the direction to decide if we add or subtract radians
        if self.turn_direction == 'left':
            self.ry -= radians
        elif self.turn_direction == 'right':
            self.ry += radians

        # Sending new rotation over websocket
        ConsumerManager().websocket.send_message(BotRotateMessage(self.id, self.ry))

    def move(self, distance: float):
        """
        Move the bot forward on X and Z axis using its current rotation.
        """

        # Calculating new coordinates
        new_x, new_z = ShapesUtils.get_coordinates_at_distance(
            origin=(self.x, self.z), distance=distance, angle=self.ry
        )

        if not self.collision():
            # Moving the bot on the map
            self.set_position(new_x, new_z, self.ry)

        # Sending new position over websocket
        ConsumerManager().websocket.send_message(BotMoveMessage(self.id, self.x, self.z))

    def send_client_bot_properties(self) -> None:
        """
        Sending bot properties to the client.
        """
        # Sending current health
        self.send_client_health_status()

        # Todo : Envoyer les caractéristiques du bots (vitesse de déplacement, etc) au client
        # Sending bot role
        # self.role

        # Sending max moving speed
        # self.moving_speed

        # Sending max turning speed
        # self.moving_speed

    def send_client_health_status(self) -> None:
        """
        Send current health to the client.
        """
        logging.debug(f"[BOT {self.name}] Health: {self.health}")

        # Sending health status to the client
        ConsumerManager().stomp.send_message(BotHealthStatusMessage(self.id, self.health))

    def _on_death(self) -> None:
        """
        Callback when the bot is dead.
        """
        if self._health <= 0:
            logging.info(f"[BOT {self.name}] Has died")

            # Stopping bot movements and threads
            self.stop()

            # Sending death information to the client
            self.send_client_health_status()
            logging.debug(f"[BOT {self.name}] Health report sent")

            # Disabling collisions
            self.set_collisions(False)
            logging.debug(f"[BOT {self.name}] Collisions disabled")

            # Send death information to display
            ConsumerManager().websocket.send_message(BotDeathMessage(self.id))

    def _on_hurt(self) -> None:
        """
        Callback when the bot is hurt.
        """
        ConsumerManager().websocket.send_message(GameObjectHurtMessage(self.id))

    def stun(self, duration_ms: float) -> None:
        """
        Stops the entity actions and stuns it.
        """
        if self.is_moving:
            self.add_command_to_queue(BotMoveCommand(priority=0, value='stop'))
        if self.is_turning:
            self.add_command_to_queue(BotTurnCommand(priority=0, value='stop'))

        # Start waiting thread
        Thread(target=self._thread_stunning, args=(duration_ms,)).start()

    def collision(self) -> bool:
        """
        Check if the bot is colliding.
        """
        if self.collision_handler.check_collision():
            self.collision_handler.handle_collision()
            return True
        return False
