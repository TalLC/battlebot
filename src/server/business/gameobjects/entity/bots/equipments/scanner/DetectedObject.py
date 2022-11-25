
class DetectedObject:

    def __init__(self, name: str | None, a_from: float, to: float, distance: float):
        self.name = name
        self.a_from = a_from
        self.to = to
        self.distance = distance
