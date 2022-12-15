from __future__ import annotations
import math
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.equipments.Equipment import Equipment

if TYPE_CHECKING:
    from business.BotManager import BotManager
    from business.gameobjects.entity.bots.equipments.scanner.SimpleScanner import SimpleScanner
    from business.gameobjects.entity.bots.equipments.weapons.BaseWeapon import BaseWeapon


class Warrior(BotModel):
    _role = "Warrior"
    _health_max: int = 100
    _moving_speed = 1.0
    _turning_speed = math.pi / 6  # 30°

    def __init__(self, bot_manager: BotManager, name: str):
        # Equipment initialization
        self._equipment = Equipment(SimpleScanner(self), BaseWeapon(self))

        super().__init__(bot_manager, name, self._role, self._health_max, self._moving_speed, self._turning_speed)

    def __str__(self):
        return f"{self.role} {self.name} ({self.id}) - " \
               f"HP: {self.health}, " \
               f"MOVING SPEED: {self.moving_speed}, " \
               f"TURNING SPEED: {self.turning_speed}"
