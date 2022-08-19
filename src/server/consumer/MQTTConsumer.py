from consumer.interfaces.IBrokerConsumer import IBrokerConsumer
from utils import mqtt


class MQTTConsumer(IBrokerConsumer):

    def __init__(self):
        self.__client = mqtt.get()

    def send_message(self, destination: str, message: str, retain: bool = False):
        """
        Send a message to a topic.
        """
        self.__client.send_message(destination, message, retain=retain)

    def close(self):
        """
        Close the MQTT client.
        """
        self.__client.close()
