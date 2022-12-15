from dataclasses import dataclass, field


@dataclass
class Target:
    id: str = field(default=None)
    x: float = field(default=0.0)
    z: float = field(default=0.0)

    def json(self):
        json = {
            'x': self.x,
            'z': self.z,
        }
        # We only add the target's id if it exists
        json |= {'id': self.id} if self.id else dict()
        return json
