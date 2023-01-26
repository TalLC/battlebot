from __future__ import annotations

import math
from random import Random
from math import pi, cos, sin
import logging
from time import time, sleep
from abc import ABC
from queue import PriorityQueue
from typing import TYPE_CHECKING
from threading import Thread, Event
from business.gameobjects.behaviour.IMoving import IMoving
from business.gameobjects.behaviour.IDestructible import IDestructible
from business.gameobjects.OrientedGameObject import OrientedGameObject
from business.ClientConnection import ClientConnection
from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.commands.BotStunCommand import BotStunCommand
from business.shapes.ShapeFactory import Shape
from business.gameobjects.entity.bots.commands.BotTurnCommand import BotTurnCommand
from business.gameobjects.entity.bots.equipments.Equipment import Equipment
from business.shapes.ShapeFactory import ShapeFactory
from business.shapes.ShapesUtils import ShapesUtils
from consumer.ConsumerManager import ConsumerManager
from business.gameobjects.tiles.Tile import Tile

from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from consumer.brokers.messages.mqtt.BotScannerDetectionMessage import BotScannerDetectionMessage
from consumer.brokers.messages.stomp.BotHealthStatusMessage import BotHealthStatusMessage
from consumer.brokers.messages.stomp.BotStunningStatusMessage import BotStunningStatusMessage
from consumer.webservices.messages.websocket.BotMoveMessage import BotMoveMessage
from consumer.webservices.messages.websocket.BotRotateMessage import BotRotateMessage
from consumer.webservices.messages.websocket.BotShootAtCoordinates import BotShootAtCoordinates
from consumer.webservices.messages.websocket.HitMessage import HitMessage
from consumer.webservices.messages.websocket.models.Target import Target

if TYPE_CHECKING:
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
        return ShapeFactory().create_shape(Shape.CIRCLE, o=(self.x, self.z), radius=.2, resolution=3)

    @shape.setter
    def shape(self, _):
        pass

    @property
    def ry_deg(self):
        return self.ry * (180 / pi)

    def __init__(self, bot_manager: BotManager, name: str, role: str, health: int, moving_speed: float,
                 turning_speed: float):
        self.bot_manager = bot_manager

        # Role name
        self._role = role

        # The equipment is defined by the bot role
        self._equipment: Equipment = Equipment()

        # Parents initializations
        OrientedGameObject.__init__(self, name)
        IMoving.__init__(self, moving_speed, turning_speed)
        IDestructible.__init__(self, health, True)

        # Random starting point
        self.x, self.z = bot_manager.game_manager.map.get_random_spawn_coordinates()
        # Random starting rotation
        self.ry = Random().randint(0, math.floor(2 * pi * 100)) / 100

        # State
        self.is_stun = False

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

        # Thread's scanner
        self._thread_scanner = Thread(
            target=self._thread_scanning,
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

    def _thread_scanning(self, e: Event):
        # Waiting interval between all increments
        loop_wait_ms = 100
        while not e.is_set():
            if self.bot_manager.game_manager.is_started and self.equipment.scanner.activated:
                detected_objects = self.equipment.scanner.scanning()
                if detected_objects:
                    ConsumerManager().mqtt.send_message(
                        BotScannerDetectionMessage(self.id, detected_object_list=detected_objects))
                sleep(self.equipment.scanner.interval)
            else:
                sleep(loop_wait_ms / 1000)

    def _thread_stunning(self, duration):

        # Envoyer un message pour dire que le bot est stun
        self.is_stun = True
        ConsumerManager().stomp.send_message(BotStunningStatusMessage(self._id, self.is_stun))
        # wait
        sleep(duration)
        self.is_stun = False
        # Envoyer un message pour dire que le bot n'est plus stun
        ConsumerManager().stomp.send_message(BotStunningStatusMessage(self._id, self.is_stun))

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

    def set_position(self, x: float, z: float, ry: float = 0.0):
        """
        Set the position and rotation of the bot.
        """
        self.x = x
        self.z = z
        self.ry = ry

    def shoot(self, angle: float) -> Target:
        """
        Called by Rest when the bot is ordered to shoot.
        Return the target that was hit (can be a GameObject or coordinates if nothing was hit).
        """
        return Target(x=0, z=0)

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
        new_x = cos(self.ry) * distance
        new_z = sin(self.ry) * distance

        if not self.collision():
            # Moving the bot on the map
            self.set_position(self.x + new_x, self.z + new_z, self.ry)

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

    def _on_hurt(self) -> None:
        """
        Callback when the bot is hurt.
        """
        ConsumerManager().websocket.send_message(HitMessage(object_type="bot", object_id=self.id))

    def collision(self):
        collision_entity = None
        neared_items = self.bot_manager.game_manager.get_items_on_map(bots_only=True, objects_only=False, radius=1,
                                                                      origin=self.coordinates)
        for item in neared_items:
            # Determine object's class
            if isinstance(item, Tile):

                if item.tile_object.has_collision and item.tile_object.shape.intersection(self.shape):
                    # Si l'objet a des collisions et si les formes de l'objet et du bot se touchent
                    collision_entity = item.tile_object.name
                    break

                elif not item.is_walkable and (self.shape.centroid.distance(item.shape.centroid) <
                                               ShapesUtils.get_radius(item.shape) + ShapesUtils.get_radius(self.shape)):
                    # Si on ne peut pas marcher sur l'item et que la distance entre l'objet et le bot est faible
                    collision_entity = item.name
                    break

            if isinstance(item, self.__class__) and item != self and item.shape.intersection(self.shape):
                # Si l'objet est un bot
                collision_entity = item.name
                break

        if collision_entity is not None:
            logging.info(f'-------------{self.name} COLLISION with {collision_entity} -------------')
            logging.info(f"before bump ({self.x} ; {self.z}")
            time_travelled = 1 / self.moving_speed
            self.add_command_to_queue(BotStunCommand(priority=0))

            Thread(target=self._thread_stunning, args=(time_travelled,)).start()

            logging.info(f"before bump ({self.x} ; {self.z}")
            logging.debug(f"orientation du bot : {math.degrees(self.ry)}, opposée : {abs(math.degrees(math.pi-self.ry))}")
            logging.debug(f"orientation du bot : {self.ry}, opposée : {math.fmod(self.ry - math.pi, 2*math.pi)}")
            dest = ShapesUtils.get_coordinates_at_distance(self.coordinates, distance=-1, angle=math.fmod(self.ry - math.pi, 2*math.pi))
            self.set_position(x=dest[0], z=dest[1], ry=self.ry)
            logging.info(f"after bump ({self.x} ; {self.z}")

            ConsumerManager().websocket.send_message(BotMoveMessage(self.id, self.x, self.z))

            return True

        return False

    def knockback(self):
        logging.debug("OOF")
        logging.debug(f"before {self.coordinates}")
        dest = ShapesUtils.get_coordinates_at_distance(origin=self.coordinates, distance=1, angle=self.ry - math.pi)
        self.set_position(x=dest[0], z=dest[1], ry=self.ry - math.pi)
        ConsumerManager().websocket.send_message(BotMoveMessage(self.id, self.x, self.z))
        ConsumerManager().websocket.send_message(BotRotateMessage(self.id, self.ry))

        logging.debug(f"after {self.coordinates}")
