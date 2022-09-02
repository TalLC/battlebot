from consumer.brokers.interfaces.IBrokerConsumer import IBrokerConsumer
from utils import stomp


class STOMPConsumer(IBrokerConsumer):

    def __init__(self):
        self.__client = stomp.get()

    def get_destination(self) -> str:
        """
        Return the root path of the topics.
        """
        return stomp.get().destination_root

    def _send_message(self, destination: str, message: dict, retain: bool = False):
        """
        Send a message to a topic.
        """
        self.__client.send_message(topic=destination, message=message)

    def close(self):
        """
        Close the STOMP client.
        """
        self.__client.close()
