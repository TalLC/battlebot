from abc import abstractmethod, ABC


class IBrokerConsumer(ABC):

    @abstractmethod
    def send_message(self, destination: str, message: str, retain: bool = False):
        """
        Send a message to a destination topic or queue.
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """
        Close the MQTT client.
        """
        raise NotImplementedError()
