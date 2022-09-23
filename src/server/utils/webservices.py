import asyncio
from time import time
from datetime import timedelta
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

    def concatenate_not(self, e: Event):
        while not e.is_set():
            if not self.__ws_tmp_queue.empty():
                message_add = self.__ws_tmp_queue.get()
                self.dispatch_message_to_all_queues([message_add])

    def concatenate(self, e: Event):
        message_list: [IWebsocketMessage] = list()
        while not e.is_set():
            try:
                timer_end = time() + timedelta(milliseconds=100).total_seconds()

                msg_count_per_bot = dict()
                while time() < timer_end:
                    message_was_updated = False
                    new_message = self.__ws_tmp_queue.get()

                    if new_message.bot_id not in msg_count_per_bot:
                        msg_count_per_bot[new_message.bot_id] = 1
                    else:
                        msg_count_per_bot[new_message.bot_id] += 1

                    if isinstance(new_message, BotUpdateMessage):
                        for prev_message in message_list:
                            if isinstance(prev_message, BotUpdateMessage):
                                if prev_message.bot_id == new_message.bot_id:
                                    prev_message += new_message
                                    message_was_updated = True
                                    break
                        if not message_was_updated:
                            message_list.append(new_message)
                    else:
                        message_list.append(new_message)

                    # asyncio.sleep(0.1)

                for key, value in msg_count_per_bot.items():
                    print(f"{key} = {value} messages concaténés en 100ms")

                self.dispatch_message_to_all_queues(message_list)
                message_list = []
            except ConnectionClosedOK:
                break

    def close_thread(self):
        self._event.set()

    def send_tmp_queue(self, message: IWebsocketMessage):
        self.__ws_tmp_queue.put(message)

    def dispatch_message_to_all_queues(self, message_list: [IWebsocketMessage]):
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
