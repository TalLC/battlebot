
class DetectedObject:

    @property
    def name(self) -> str:
        return self._name

    @property
    def angle(self) -> int:
        return self._angle

    def __init__(self, name: str, angle: int):
        self._name = name
        self._angle = angle
