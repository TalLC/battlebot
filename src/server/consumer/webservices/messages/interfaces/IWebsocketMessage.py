from abc import abstractmethod, ABC


class IWebsocketMessage(ABC):

    @abstractmethod
    def json(self) -> dict:
        raise NotImplementedError()
