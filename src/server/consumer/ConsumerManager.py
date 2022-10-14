import logging
from consumer.brokers.STOMPConsumer import STOMPConsumer
from consumer.brokers.MQTTConsumer import MQTTConsumer
from consumer.webservices.WebsocketConsumer import WebsocketConsumer
from common.Singleton import SingletonABCMeta


class ConsumerManager(metaclass=SingletonABCMeta):
    """
    Start all consumer services.
    - STOMP
    - MQTT
    - Websocket
    """

    @property
    def mqtt(self):
        """
        Return the MQTT client instance.
        """
        return self.__mqtt

    @property
    def stomp(self):
        """
        Return the STOMP client instance.
        """
        return self.__stomp

    @property
    def websocket(self):
        """
        Return the Websocket consumer instance.
        """
        return self.__websocket

    def start_all(self):
        self.__start_mqtt()
        self.__start_stomp()
        self.__start_websocket()

    def __start_mqtt(self):
        logging.info("[CONSUMER_MANAGER] Starting MQTT")
        self.__mqtt = MQTTConsumer()

    def __start_stomp(self):
        logging.info("[CONSUMER_MANAGER] Starting STOMP")
        self.__stomp = STOMPConsumer()

    def __start_websocket(self):
        logging.info("[CONSUMER_MANAGER] Starting Websocket")
        self.__websocket = WebsocketConsumer()

    def close(self):
        self.__mqtt.close()
        self.__stomp.close()
