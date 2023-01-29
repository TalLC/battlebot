from __future__ import annotations
import math
from typing import TYPE_CHECKING
from business.shapes.ShapeFactory import Shape
from business.gameobjects.entity.bots.models.BotModel import BotModel
from business.gameobjects.entity.bots.equipments.Equipment import Equipment
from business.gameobjects.entity.bots.equipments.scanner.SimpleScanner import SimpleScanner
from business.gameobjects.entity.bots.equipments.weapons.BaseWeapon import BaseWeapon

if TYPE_CHECKING:
    from business.BotManager import BotManager


class Warrior(BotModel):
    _role = "Warrior"
    _model_name = "default"
    _health_max: int = 100
    _moving_speed = 1.0
    _turning_speed = math.pi / 6  # 30°
    _shape_name = "CIRCLE"
    _shape_size = 0.2

    @property
    def model_name(self) -> str:
        return self._model_name

    def __init__(self, bot_manager: BotManager, name: str):
        super().__init__(bot_manager, name, self._role, self._health_max, self._moving_speed, self._turning_speed,
                         self._shape_name, self._shape_size)

        # Equipment initialization
        self._equipment = Equipment(SimpleScanner(self), BaseWeapon(self))

    def __str__(self):
        return f"{self.role} {self.name} ({self.id}) - " \
               f"HP: {self.health}, " \
               f"MOVING SPEED: {self.moving_speed}, " \
               f"TURNING SPEED: {self.turning_speed}, " \
               f"SCANNER: {self.equipment.scanner}, " \
               f"WEAPON: {self.equipment.weapon}"
