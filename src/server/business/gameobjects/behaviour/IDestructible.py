
class IDestructible:
    _HEALTH_MAX = 0
    _HEALTH = 0
    _HAS_COLLISION = False

    @property
    def health(self) -> int:
        return self._HEALTH

    @property
    def health_max(self) -> int:
        return self._HEALTH_MAX

    @property
    def is_alive(self) -> bool:
        return self._HEALTH > 0

    @property
    def has_collision(self) -> bool:
        return self._HAS_COLLISION

    def __init__(self, health: int = 0, has_collision: bool = False):
        self._HEALTH_MAX = health
        self._HEALTH = self._HEALTH_MAX
        self._HAS_COLLISION = has_collision

    def set_collisions(self, has_collision: bool) -> None:
        """
        Set the collisions of the entity.
        """
        self._HAS_COLLISION = has_collision

    def heal(self, health: int) -> None:
        """
        Heal the entity.
        """
        if 0 < self._HEALTH < self._HEALTH_MAX:
            self._HEALTH += health
            if self._HEALTH > self._HEALTH_MAX:
                self._HEALTH = self._HEALTH_MAX

    def hurt(self, damage: int) -> None:
        """
        Apply damages to the entity.
        """
        if self._HEALTH > 0:
            self._HEALTH -= damage
            if self._HEALTH < 0:
                self._HEALTH = 0
                self._on_death()

    def _on_death(self) -> None:
        """
        Callback when the entity is dead.
        Disable collisions if the entity is dead.
        """
        if self._HEALTH <= 0:
            # entity is dead
            self.set_collisions(False)
