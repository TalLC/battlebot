import time
from queue import SimpleQueue
from threading import Thread, Event
from typing import List

from websockets.exceptions import ConnectionClosedOK

from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage
from common.Singleton import SingletonABCMeta
from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class Webservices(metaclass=SingletonABCMeta):
    __ws_client_queues: [SimpleQueue] = list()
    __ws_tmp_queue = SimpleQueue()

    def __init__(self):
        self._event = Event()
        self._thread = Thread(target=self.concatenate, args=[self._event])
        self._thread.start()

    def concatenate(self, e: Event):
        message_list: [IWebsocketMessage] = list()
        while not e.is_set():
            try:
                timer = time.time()
                while time.time() - timer > 100:
                    maj = False
                    message_add = self.__ws_tmp_queue.get()
                    if isinstance(message_add, BotUpdateMessage):
                        for message in message_list:
                            if isinstance(message, BotUpdateMessage):
                                if message.bot_id == message_add.bot_id:
                                    message += message_add
                                    maj = True
                                    break
                        if not maj:
                            message_list.append(message_add)
                    else:
                        message_list.append(message_add)
                self.dispatch_message_to_all_queues(message_list)
                message_list = []
            except ConnectionClosedOK:
                break

    def close_thread(self):
        self._event.set()

    def send_tmp_queue(self, message: IWebsocketMessage):
        self.__ws_tmp_queue.put(message)

    def dispatch_message_to_all_queues(self, message_list: List[IWebsocketMessage]):
        for message in message_list:
            for queue in self.__ws_client_queues:
                queue.put(item=message)

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
