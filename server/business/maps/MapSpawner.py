from dataclasses import dataclass, field


@dataclass
class MapSpawner:
    team_id: int
    x: float
    z: float
    ry: float

    def json(self):
        return {
            'team_id': self.team_id,
            'x': self.x,
            'z': self.z,
            'ry': self.ry
        }
