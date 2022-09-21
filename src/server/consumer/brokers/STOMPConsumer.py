from consumer.brokers.interfaces.IBrokerConsumer import IBrokerConsumer
from utils.stomp import STOMP


class STOMPConsumer(IBrokerConsumer):

    def __init__(self):
        self.__client = STOMP()

    def get_destination(self) -> str:
        """
        Return the root path of the topics.
        """
        return self.__client.destination_root

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
