from business.gameobjects.entity.bots.Bot import Bot


class Warrior(Bot):
    _HEALTH_MAX: int = 100
    _SPEED = 1.0

    def __init__(self, name: str):
        super().__init__(name, self._HEALTH_MAX, self._SPEED)

    def __str__(self):
        return f"{self.name} ({self.id}) - HP: {self.health}, SPEED: {self.speed}"
    