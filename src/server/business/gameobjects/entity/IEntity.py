from abc import ABC


class IEntity(ABC):
    _NAME = str()

    @property
    def name(self) -> str:
        return self._NAME

    def __init__(self, name: str):
        self._NAME = name
