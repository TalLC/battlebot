import logging
from utils.mqtt import MQTT


class MQTTProvider:

    def is_connected(self) -> bool:
        return self.__client.is_connected

    def __init__(self):
        self.__client = MQTT()

    def on_message(self, func):
        """
        Register a callback function to be called when a message is received.
        """
        self.__client.on_message = func
 
    def subscribe(self, destination: str):
        """
        Subscribe to a topic and receive incoming messages.
        """
        self.__client.subscribe(destination=destination)
        logging.info(f"Subscribed to topic {destination}")

    def loop(self):
        """
        Run the MQTT client loop to read messages.
        """
        self.__client.loop()

    def close(self):
        """
        Close the MQTT client.
        """
        self.__client.close()
