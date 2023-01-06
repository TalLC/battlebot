from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.equipments.weapons.interface.IWeapon import IWeapon

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

    def __init__(self, bot: BotModel, name: str, damages: int, reach_distance: int):
        self._bot = bot
        self._name = name
        self._damages = damages
        self._reach_distance = reach_distance

    def __str__(self) -> str:
        return f"{self.name} (damages: {self.damages}, reach: {self.reach_distance})"
