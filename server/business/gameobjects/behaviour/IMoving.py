from __future__ import annotations

from abc import ABC
from time import sleep
from threading import Thread
from typing import TYPE_CHECKING

from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.BotStunningStatusMessage import BotStunningStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.OrientedGameObject import OrientedGameObject


class IMoving(ABC):

    @property
    def entity(self) -> OrientedGameObject:
        """
        Parent entity.
        """
        return self._entity

    @property
    def is_moving(self) -> bool:
        """
        Is the entity moving?
        """
        return self._is_moving

    @property
    def is_stunned(self) -> bool:
        """
        Is the entity stunned? (cannot move)
        """
        return self._is_stunned

    @property
    def moving_speed(self) -> float:
        """
        Speed in point per seconds.
        """
        return self._moving_speed

    @property
    def is_turning(self) -> bool:
        """
        Is the entity turning?
        """
        return self._is_turning

    @property
    def turn_direction(self) -> str:
        """
        Return which direction the entity is turning to.
        """
        return self._turn_direction

    @property
    def turning_speed(self) -> float:
        """
        Rotating speed in radians per seconds.
        """
        return self._turning_speed

    def __init__(self, entity: OrientedGameObject, moving_speed: float = 1.0, turning_speed: float = 0.1):
        self._entity = entity
        self._is_moving = False
        self._is_turning = False
        self._is_stunned = False
        self._turn_direction = str()
        self._moving_speed = moving_speed
        self._turning_speed = turning_speed

        # Last entity move timestamp
        self.last_move_timestamp = 0.0

        # Last entity turn timestamp
        self.last_turn_timestamp = 0.0

    def _thread_stunning(self, duration_ms: int):
        """
        Stop the bot from moving for the specified duration.
        """
        # Envoyer un message pour dire que le bot est stun
        self._is_stunned = True
        ConsumerManager().stomp.send_message(BotStunningStatusMessage(self.entity.id, self.is_stunned))
        # wait
        sleep(duration_ms)
        self._is_stunned = False
        # Envoyer un message pour dire que le bot n'est plus stun
        ConsumerManager().stomp.send_message(BotStunningStatusMessage(self.entity.id, self.is_stunned))

    def set_moving(self, state: bool):
        """
        Set the entity to moving or stopped.
        """
        self.last_move_timestamp = 0.0
        self._is_moving = state

    def set_turning(self, state: bool, direction: str = str()):
        """
        Set the entity to turn or go straight.
        """
        self.last_turn_timestamp = 0.0
        self._is_turning = state
        self._turn_direction = direction

    @staticmethod
    def get_distance_from_time_and_speed(moving_speed: float, elapsed_time_secs: float) -> float:
        """
        Return the traveled distance for an amount of time.
        """
        return moving_speed * elapsed_time_secs

    @staticmethod
    def get_turn_from_time_and_speed(turning_speed: float, elapsed_time_secs: float) -> float:
        """
        Return the rotation in radians for an amount of time.
        """
        return turning_speed * elapsed_time_secs

    def stun(self, duration_ms: float) -> None:
        """
        Stops the entity actions and stuns it.
        """
        self._is_moving = False
        self._is_turning = False

        # Start waiting thread
        Thread(target=self._thread_stunning, args=(duration_ms,)).start()
