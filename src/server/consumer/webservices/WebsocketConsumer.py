from consumer.webservices.messages.interfaces.IWebsocketMessage import IWebsocketMessage
from utils.webservices import Webservices


class WebsocketConsumer:

    def __init__(self):
        self.__webservices = Webservices()

    def send_message(self, message: IWebsocketMessage):
        self.__webservices.send_to_all_queues(message)
