from abc import ABC


class IMoving(ABC):

    @property
    def speed(self) -> float:
        return self._SPEED

    def __init__(self, speed: float = 1.0):
        self._SPEED = speed
