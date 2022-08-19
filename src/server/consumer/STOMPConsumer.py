from utils import stomp


class STOMPConsumer:

    def __init__(self):
        self.__client = stomp.get()

    def send_message(self, topic: str, message: str):
        """
        Send a message to a topic.
        """
        self.__client.send_message(topic=topic, message=message)

    def close(self):
        """
        Close the STOMP client.
        """
        self.__client.close()
