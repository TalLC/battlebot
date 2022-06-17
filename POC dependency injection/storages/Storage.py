import abc


class SingletonABCMeta(abc.ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Storage(abc.ABC):
    __metaclass__ = SingletonABCMeta

    @abc.abstractmethod
    def add(self, item: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, pk: int):
        raise NotImplementedError


