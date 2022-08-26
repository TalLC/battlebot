from abc import abstractmethod, ABC
from consumer.actions.interfaces.IAction import IAction


class IBrokerConsumer(ABC):

    def send_action(self, action: IAction):
        """
        Send an action to the correct topic or queue.
        """
        self._send_message(self.get_destination(), action.get_message())

    @abstractmethod
    def get_destination(self) -> str:
        """
        Return the base name of the queue or topic.
        """
        raise NotImplementedError()

    @abstractmethod
    def _send_message(self, destination: str, message: dict, retain: bool = False):
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
