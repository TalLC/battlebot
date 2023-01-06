from __future__ import annotations
from typing import TYPE_CHECKING
from common.Singleton import SingletonABCMeta
from business.gameobjects.entity.bots.equipments.weapons.models.WeaponModel import WeaponModel
from business.gameobjects.entity.bots.equipments.weapons.BaseWeapon import BaseWeapon

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class WeaponFactory(metaclass=SingletonABCMeta):

    @staticmethod
    def create_weapon(bot: BotModel, weapon_type: str) -> WeaponModel:
        """
        Create a new weapon and return the object.
        """
        if weapon_type.lower() == "base":
            return BaseWeapon(bot)
        else:
            return BaseWeapon(bot)
