import json
import logging
import stomp
from stomp import ConnectionListener
from stomp.utils import Frame
from provider.brokers.config.STOMPConfig import STOMPConfig


class STOMP:
    ConnectionListener = ConnectionListener
    Frame = Frame

    @property
    def is_connected(self) -> bool:
        """
        Is set to True when the client is connected to the broker.
        """
        return self.__connected

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port

    @property
    def destination_root(self) -> str:
        return self.__destination_root

    def __init__(self):
        self.__connected = False
        self.__host = STOMPConfig.host
        self.__port = STOMPConfig.port
        self.__destination_root = STOMPConfig.destination_root
        self.__subscription_id = 0

        # STOMP client
        self.__client = stomp.Connection(host_and_ports=[(self.__host, self.__port)])

        # Connecting client
        self.__client.connect(username=STOMPConfig.username, passcode=STOMPConfig.password, wait=True)
        self.__connected = True

    def send_message(self, topic: str, message: dict):
        """
        Send a message to a topic.
        """
        self.__client.send(destination=topic, body=json.dumps(message))

    def subscribe(self, destination: str):
        """
        Subscribe to a topic and receive incoming messages.
        """
        self.__subscription_id += 1
        self.__client.subscribe(destination=destination, id=str(self.__subscription_id))
        logging.info(f"Subscribed to queue {destination}")

    def set_listener(self, name: str, listener: stomp.ConnectionListener):
        """
        Set a listener for the STOMP client.
        """
        self.__client.set_listener(name, listener)

    def close(self):
        """
        Close the connection to the broker.
        """
        self.__client.disconnect()
        logging.info("STOMP client disconnected")
