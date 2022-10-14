from time import time
from datetime import timedelta
from queue import SimpleQueue
from threading import Thread, Event
from common.Singleton import SingletonABCMeta
from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage
from consumer.webservices.messages.websocket.models.BotUpdateMessage import BotUpdateMessage


class Webservices(metaclass=SingletonABCMeta):
    __ws_client_queues: [SimpleQueue] = list()
    __ws_tmp_queue = SimpleQueue()

    def __init__(self):
        self._event = Event()
        self._thread = Thread(target=self.concatenate, args=[self._event])
        self._thread.start()

    def concatenate(self, e: Event):
        # Message gathering interval
        loop_wait_ms = 100

        # Message gathered and concatenated in the interval
        message_list: [IWebsocketMessage] = list()

        while not e.is_set():
            # End of this loop in Now + loop_wait_ms
            timer_end = time() + timedelta(milliseconds=loop_wait_ms).total_seconds()

            # Get all messages in this interval and concatenates the ones that can be
            while time() < timer_end:

                # Gathering a message
                new_message = self.__ws_tmp_queue.get()
                has_been_merged = False

                # Checking type of message
                if isinstance(new_message, BotUpdateMessage):

                    # Checking if we had another message from the same bot in the past
                    for prev_message in message_list:

                        # If it was a message of type BotUpdateMessage, it can be concatenated
                        if isinstance(prev_message, BotUpdateMessage):

                            # We already had a message from this bot, let's add them
                            if prev_message.bot_id == new_message.bot_id:
                                prev_message += new_message
                                has_been_merged = True
                                continue

                # We cannot merge this message with a previous one, adding it to the list
                if not has_been_merged:
                    message_list.append(new_message)

            # Sending message to all displays
            self.dispatch_message_to_all_queues(message_list)
            message_list = []

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
