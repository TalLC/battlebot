from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.equipments.weapons.models.WeaponModel import WeaponModel

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class BaseWeapon(WeaponModel):
    _name = "Basic weapon"
    _damages: int = 5
    _reach_distance: int = 3

    def __init__(self, bot: BotModel):
        super().__init__(bot, self._name, self._damages, self._reach_distance)
