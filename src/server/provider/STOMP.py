import logging
import stomp


class STOMP:
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

    def __init__(self, host: str, port: int, username: str, password: str):
        self.__connected = False
        self.__host = host
        self.__port = port

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

    def close(self):
        """
        Close the connection to the broker.
        """
        self.__client.disconnect()
        logging.info("STOMP client disconnected")
