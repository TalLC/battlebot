from consumer.brokers.interfaces.IBrokerConsumer import IBrokerConsumer
from utils import mqtt


class MQTTConsumer(IBrokerConsumer):

    def __init__(self):
        self.__client = mqtt.get()

    def get_destination(self) -> str:
        """
        Return the root path of the topics.
        """
        return mqtt.get().destination_root

    def _send_message(self, destination: str, message: dict, retain: bool = False):
        """
        Send a message to a topic.
        """
        self.__client.send_message(topic=destination, message=message, retain=retain)

    def close(self):
        """
        Close the MQTT client.
        """
        self.__client.close()
