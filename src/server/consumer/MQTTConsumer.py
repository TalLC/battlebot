import logging
from utils import mqtt


class MQTTConsumer:

    def __init__(self):
        self.__client = mqtt.get()

    @staticmethod
    def on_publish(_client, _userdata, mid: int):
        """
        Callback function when a message is published.
        """
        logging.debug(f"Message id {mid} published")

    def send_message(self, topic: str, message: str, retain: bool = False):
        """
        Send a message to a topic.
        """
        self.__client.send_message(topic, message, retain=retain)

    def close(self):
        """
        Close the MQTT client.
        """
        self.__client.close()
