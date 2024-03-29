from abc import ABC, abstractmethod
from threading import Thread
from time import sleep


class IDestructible(ABC):
    _health_max = 0
    _health = 0
    _has_collision = False

    @property
    def health(self) -> int:
        return self._health

    @property
    def health_max(self) -> int:
        return self._health_max

    @property
    def is_alive(self) -> bool:
        return self._health > 0

    @property
    def has_collision(self) -> bool:
        return self._has_collision

    def __init__(self, health: int = 0, has_collision: bool = False):
        self._health_max = health
        self._health = self._health_max
        self._has_collision = has_collision

    def set_collisions(self, has_collision: bool) -> None:
        """
        Set the collisions of the entity.
        """
        self._has_collision = has_collision

    def heal(self, health: int) -> None:
        """
        Heal the entity.
        """
        if 0 < self._health < self._health_max:
            self._health += health
            if self._health > self._health_max:
                self._health = self._health_max

    def hurt(self, damage: int) -> None:
        """
        Apply damages to the entity.
        """
        Thread(target=self.thread_hurt_delay, args=(damage,)).start()

    def thread_hurt_delay(self, damage: int) -> None:
        """
        Apply delay for animation front bullet.
        """
        sleep(0.2)
        if self._health > 0:
            self._health -= damage
            if self._health <= 0:
                self._health = 0
                self.set_collisions(False)
                self._on_death()
                return
            self._on_hurt()

    def kill(self) -> None:
        """
        Kills the entity.
        """
        self.hurt(self._health_max)

    @abstractmethod
    def _on_death(self) -> None:
        """
        Callback when the entity is dead.
        """
        raise NotImplementedError

    @abstractmethod
    def _on_hurt(self) -> None:
        """
        Callback when the entity is hurt.
        """
        raise NotImplementedError
