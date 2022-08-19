import logging
from STOMPConsumer import STOMPConsumer
from MQTTConsumer import MQTTConsumer
from common.Singleton import SingletonABCMeta


class ConsumerManager(metaclass=SingletonABCMeta):
    """
    Start all consumer services.
    - Rest API
    - STOMP
    - MQTT
    """
    def start_all(self):
        self.__start_mqtt()
        self.__start_stomp()

    def __start_mqtt(self):
        logging.info("Starting MQTT")
        self.mqtt = MQTTConsumer()

    def __start_stomp(self):
        logging.info("Starting STOMP")
        self.stomp = STOMPConsumer()

    def close(self):
        self.mqtt.close()
        self.stomp.close()

    def mqtt(self):
        """
        Return the MQTT client instance.
        """
        return self.mqtt

    def stomp(self):
        """
        Return the STOMP client instance.
        """
        return self.stomp
