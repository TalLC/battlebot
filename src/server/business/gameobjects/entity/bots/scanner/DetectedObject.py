
class DetectedObject:

    @property
    def name(self) -> str:
        return self._name

    @property
    def angle(self) -> float:
        return self._angle

    def __init__(self, name: str, angle: float, distance: float):
        self._name = name
        self._angle = angle
        self._distance = distance
