import abc


class Writer(abc.ABC):

    @abc.abstractmethod
    def write(self, item: str):
        raise NotImplementedError
