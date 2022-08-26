from consumer.interfaces.IBrokerConsumer import IBrokerConsumer
from utils import stomp
import json


class STOMPConsumer(IBrokerConsumer):

    def get_destination(self) -> str:
        return stomp.get().destination_root

    def __init__(self):
        self.__client = stomp.get()

    def _send_message(self, destination: str, message: dict, retain: bool = False):
        """
        Send a message to a topic.
        """
        self.__client.send_message(topic=destination, message=json.dumps(message))

    def close(self):
        """
        Close the STOMP client.
        """
        self.__client.close()
