import math

from business.gameobjects.entity.bots.models.BotModel import BotModel


class Warrior(BotModel):
    _role = "Warrior"
    _health_max: int = 100
    _moving_speed = 1.0
    _turning_speed = math.pi / 6  # 30°

    def __init__(self, name: str):
        super().__init__(name, self._role, self._health_max, self._moving_speed, self._turning_speed)

    def __str__(self):
        return f"{self.role} {self.name} ({self.id}) - " \
               f"HP: {self.health}, " \
               f"MOVING SPEED: {self.moving_speed}, " \
               f"TURNING SPEED: {self.turning_speed}"
