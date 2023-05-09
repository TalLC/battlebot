import logging
from abc import abstractmethod, ABC

from common.PerformanceCounter import PerformanceCounter
from consumer.brokers.messages.interfaces.IMessage import IMessage


class IBrokerConsumer(ABC):

    @PerformanceCounter.count
    def send_message(self, message: IMessage):
        """
        Send an action to the correct topic or queue.
        """
        logging.debug(f"[BROKER] Sending '{message.msg_type}' message: {message.json()}")
        self._send_message(f'{self.get_destination()}{message.bot_id}', message.json(), message.retain)

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
