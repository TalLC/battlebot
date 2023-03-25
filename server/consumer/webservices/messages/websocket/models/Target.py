from dataclasses import dataclass, field


@dataclass
class Target:
    id: str = field(default=None)
    x: float = field(default=None)
    z: float = field(default=None)

    def json(self):
        json = dict()
        json |= {'id': self.id} if self.id else dict()
        json |= {'x': self.x} if self.x is not None else dict()
        json |= {'z': self.z} if self.z is not None else dict()
        return json
