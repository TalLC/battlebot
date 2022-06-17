import abc


class Storage(abc.ABC):

    @abc.abstractmethod
    def add(self, item: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, pk: int):
        raise NotImplementedError


