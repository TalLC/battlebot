from __future__ import annotations
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.equipments.weapons.models.WeaponModel import WeaponModel

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class SmokeGrenade(WeaponModel):
    _name = "Smoke grenade"
    _damages: int = 0
    _reach_distance: int = 5

    def __init__(self, bot: BotModel):
        super().__init__(bot, self._name, self._damages, self._reach_distance)
