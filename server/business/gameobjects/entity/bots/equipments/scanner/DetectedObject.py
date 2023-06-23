from math import radians
from business.shapes.ShapesUtils import ShapesUtils


class DetectedObject:

    def __init__(self, obj_id: str, name: str | None, object_type: str, a_from: float, a_to: float, distance: float,
                 origin: tuple, origin_ry: float):
        self.id = obj_id
        self.name = name
        self.object_type = object_type
        self.a_from = a_from
        self.a_to = a_to
        self.distance = distance

        # Debug usage only
        self.origin = origin
        self.origin_ry = origin_ry
        self.x, self.z = ShapesUtils.get_coordinates_at_distance(
            origin=(self.origin[0][0], self.origin[1][0]),
            distance=self.distance,
            angle=self.origin_ry + (radians(self.a_from) + radians(self.a_to)) / 2,
            is_degrees=False
        )

    def json(self):
        return {
            "from": self.a_from,
            "to": self.a_to,
            "name": self.name,
            "object_type": self.object_type,
            "distance": self.distance
        }

    def __str__(self):
        return f"{self.name} ({self.object_type}) : from {self.a_from} to {self.a_to} at {self.distance}."

    def __repr__(self):
        return f"{self.name}:{self.a_from}->{self.a_to}|{self.distance}"
