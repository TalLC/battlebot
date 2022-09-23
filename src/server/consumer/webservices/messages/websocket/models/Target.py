from dataclasses import dataclass


@dataclass
class Target:
    x: float
    z: float

    def json(self):
        return {'x': self.x, 'z': self.z}
