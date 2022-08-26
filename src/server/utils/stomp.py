import json
import logging
from pathlib import Path
import stomp
from stomp import ConnectionListener
from stomp.utils import Frame


__instance = None
config = json.loads(Path('conf', '../conf/stomp.json').read_text())


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

    def __init__(self, host: str, port: int, username: str, password: str, destination_root: str):
        self.__connected = False
        self.__host = host
        self.__port = port
        self.__destination_root = destination_root
        self.__subscription_id = 0

        # STOMP client
        self.__client = stomp.Connection(host_and_ports=[(self.__host, self.__port)])

        # Connecting client
        self.__client.connect(username=username, passcode=password, wait=True)  # Throw exception if failed to connect
        self.__connected = True

    def send_message(self, topic: str, message: str):
        """
        Send a message to a topic.
        """
        self.__client.send(destination=topic, body=message)

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


def get() -> STOMP:
    """
    Get STOMP instance.
    """
    global __instance

    if __instance is None:
        __instance = STOMP(
            host=config['host'],
            port=config['port'],
            username=config['username'],
            password=config['password'],
            destination_root=config['destination_root']
        )

    return __instance
