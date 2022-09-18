import logging
from utils.stomp import STOMP


class STOMPProvider:

    @property
    def is_connected(self) -> bool:
        return self.__client.is_connected

    def __init__(self):
        self.__client = STOMP()
 
    def subscribe(self, destination: str):
        """
        Subscribe to a topic and receive incoming messages.
        """
        self.__client.subscribe(destination=destination)
        logging.info(f"Subscribed to topic {destination}")

    def set_listener(self, name: str, listener: STOMP.ConnectionListener):
        """
        Set a listener for the STOMP client.
        """
        self.__client.set_listener(name, listener)
    
    def close(self):
        """
        Close the connection to the broker.
        """
        self.__client.close()
