from consumer.interfaces.IBrokerConsumer import IBrokerConsumer
from utils import stomp


class STOMPConsumer(IBrokerConsumer):

    def __init__(self):
        self.__client = stomp.get()

    def send_message(self, destination: str, message: str, retain: bool = False):
        """
        Send a message to a topic.
        """
        self.__client.send_message(topic=destination, message=message)

    def close(self):
        """
        Close the STOMP client.
        """
        self.__client.close()
