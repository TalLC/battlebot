
class DetectedObject:

    def __init__(self, obj_id: str, name: str | None, object_type: str, a_from: float, a_to: float, distance: float):
        self.id = obj_id
        self.name = name
        self.object_type = object_type
        self.a_from = a_from
        self.a_to = a_to
        self.distance = distance

    def __str__(self):
        return f"{self.name} ({self.object_type}) : from {self.a_from} to {self.a_to} at {self.distance}."

    def __repr__(self):
        return f"{self.name}:{self.a_from}->{self.a_to}|{self.distance}"
