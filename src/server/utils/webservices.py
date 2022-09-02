import logging
from queue import SimpleQueue

from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage
from common.Singleton import SingletonABCMeta


class Webservices(metaclass=SingletonABCMeta):
    __ws_client_queues = []

    def __init__(self):
        ...

    def send_to_all_queues(self, message: IWebsocketMessage):
        pass

    def add_ws_queue(self, queue: SimpleQueue):
        """
        Add a webservices client message queue.
        """
        self.__ws_client_queues.append(queue)

    def remove_ws_queue(self, queue: SimpleQueue):
        """
        Remove the webservices client message queue.
        """
        self.__ws_client_queues.remove(queue)
