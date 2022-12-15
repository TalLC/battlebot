from abc import ABC, abstractmethod
from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage


class ICoordinatesMessage(IWebsocketMessage, ABC):

    @abstractmethod
    def coordinates(self):
        NotImplementedError()

    def __init__(self, msg_type: str):
        super().__init__(msg_type)

    @abstractmethod
    def __add__(self, other):
        NotImplementedError()

    @abstractmethod
    def json(self):
        NotImplementedError()
