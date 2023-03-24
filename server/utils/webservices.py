from time import time, sleep
from datetime import timedelta
from queue import SimpleQueue
from threading import Thread, Event
from common.Singleton import SingletonABCMeta
from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage
from consumer.webservices.messages.websocket.BotUpdateMessage import BotUpdateMessage


class Webservices(metaclass=SingletonABCMeta):
    __ws_client_queues: [SimpleQueue] = list()
    __ws_tmp_queue = SimpleQueue()

    def __init__(self):
        self._event = Event()
        self._thread = Thread(target=self.concatenate, args=[self._event])
        self._thread.start()

    def concatenate(self, e: Event):
        # We concatenate loop_wait_ms of incoming messages
        loop_wait_ms = 100

        # We read the queue every reading_interval_ms
        # ie: we can read a maximum of "loop_wait_ms / reading_interval_ms" messages in 1 loop
        reading_interval_ms = 1

        # Message gathered and concatenated in the interval
        message_list: [IWebsocketMessage] = list()

        while not e.is_set():
            # End of this loop in Now + loop_wait_ms
            timer_end = time() + timedelta(milliseconds=loop_wait_ms).total_seconds()

            # Get all messages in this interval and concatenates the ones that can be
            while time() < timer_end:

                # Gathering a message
                while not self.__ws_tmp_queue.empty():
                    new_message = self.__ws_tmp_queue.get(block=False)
                    has_been_merged = False

                    # Checking type of message
                    if isinstance(new_message, BotUpdateMessage):

                        # Checking if we had another message from the same bot in the past
                        for prev_message in message_list:

                            # If it was a message of type BotUpdateMessage, it can be concatenated
                            if isinstance(prev_message, BotUpdateMessage):

                                # We already had a message from this bot, let's add them
                                if prev_message.id == new_message.id:
                                    prev_message += new_message
                                    has_been_merged = True
                                    continue

                    # We cannot merge this message with a previous one, adding it to the list
                    if not has_been_merged:
                        message_list.append(new_message)

                sleep(reading_interval_ms / 1000)

            # Sending message to all displays
            if len(message_list):
                self.dispatch_message_to_all_queues(message_list)
                message_list = []

    # def concatenate(self, e: Event):
    #     # Message gathering interval
    #     loop_wait_ms = 100
    #
    #     # Message gathered and concatenated in the interval
    #     message_list: [IWebsocketMessage] = list()
    #
    #     while not e.is_set():
    #         # End of this loop in Now + loop_wait_ms
    #         timer_end = time() + timedelta(milliseconds=loop_wait_ms).total_seconds()
    #
    #         # Get all messages in this interval and concatenates the ones that can be
    #         while time() < timer_end:
    #
    #             # Gathering a message
    #             new_message = self.__ws_tmp_queue.get()
    #             has_been_merged = False
    #
    #             # Checking type of message
    #             if isinstance(new_message, BotUpdateMessage):
    #
    #                 # Checking if we had another message from the same bot in the past
    #                 for prev_message in message_list:
    #
    #                     # If it was a message of type BotUpdateMessage, it can be concatenated
    #                     if isinstance(prev_message, BotUpdateMessage):
    #
    #                         # We already had a message from this bot, let's add them
    #                         if prev_message.id == new_message.id:
    #                             prev_message += new_message
    #                             has_been_merged = True
    #                             continue
    #
    #             # We cannot merge this message with a previous one, adding it to the list
    #             if not has_been_merged:
    #                 message_list.append(new_message)
    #
    #         # Sending message to all displays
    #         if len(message_list):
    #             self.dispatch_message_to_all_queues(message_list)
    #             message_list = []

    def close_thread(self):
        self._event.set()

    def send_tmp_queue(self, message: IWebsocketMessage):
        self.__ws_tmp_queue.put(message)

    def dispatch_message_to_all_queues(self, message_list: [IWebsocketMessage]):
        json_messages = [message.json() for message in message_list]

        json_enveloppe = {
            'messages': json_messages,
            'count': len(json_messages)
        }
        for queue in self.__ws_client_queues:
            queue.put(item=json_enveloppe)

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
