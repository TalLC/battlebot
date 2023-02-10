from __future__ import annotations

import logging
from abc import ABC
from threading import Thread
from time import sleep
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.equipments.weapons.interface.IWeapon import IWeapon
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.BotWeaponStatusMessage import BotWeaponStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class WeaponModel(IWeapon, ABC):

    @property
    def bot(self) -> BotModel:
        return self._bot

    @property
    def name(self) -> str:
        return self._name

    @property
    def damages(self) -> int:
        return self._damages

    @property
    def reach_distance(self) -> int:
        return self._reach_distance

    @property
    def can_shoot(self):
        return self._can_shoot

    def __init__(self, bot: BotModel, name: str, damages: int, reach_distance: int, cooldown_ms: int):
        self._bot = bot
        self._name = name
        self._damages = damages
        self._reach_distance = reach_distance
        self._cooldown_ms = cooldown_ms
        self._can_shoot: bool = True

    def __str__(self) -> str:
        return f"{self.name} (damages: {self.damages}, reach: {self.reach_distance}), cooldown: {self._cooldown_ms / 1000}"

    def _thread_reload(self, duration_ms: int):
        """
            Stop the weapon from shooting for the specified duration.
        """
        # Envoyer un message pour dire que l'arme n'est plus disponible
        self._can_shoot = False
        ConsumerManager().stomp.send_message(BotWeaponStatusMessage(self._bot.id, self._can_shoot))
        # wait
        sleep(duration_ms / 1000)
        # Envoyer un message pour dire que l'arme est de nouveau disponible
        self._can_shoot = True
        ConsumerManager().stomp.send_message(BotWeaponStatusMessage(self._bot.id, self._can_shoot))

    def reload(self):
        """
            Block usage weapons .
        """
        # Start waiting thread
        Thread(target=self._thread_reload, args=(self._cooldown_ms,)).start()
