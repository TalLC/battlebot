import logging
from consumer.STOMPConsumer import STOMPConsumer
from consumer.MQTTConsumer import MQTTConsumer
from common.Singleton import SingletonABCMeta


class ConsumerManager(metaclass=SingletonABCMeta):
    """
    Start all consumer services.
    - Rest API
    - STOMP
    - MQTT
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

    def start_all(self):
        self.__start_mqtt()
        self.__start_stomp()

    def __start_mqtt(self):
        logging.info("Starting MQTT")
        self.__mqtt = MQTTConsumer()

    def __start_stomp(self):
        logging.info("Starting STOMP")
        self.__stomp = STOMPConsumer()

    def close(self):
        self.__mqtt.close()
        self.__stomp.close()
