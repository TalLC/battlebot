from dataclasses import dataclass, field


@dataclass
class MapName:
    id: str
    name: str

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }
