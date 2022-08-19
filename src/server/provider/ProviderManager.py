import logging
from provider.RestAPI import RestAPI
from common.Singleton import SingletonABCMeta
from provider.MQTTProvider import MQTTProvider
from provider.STOMPProvider import STOMPProvider


class ProviderManager(metaclass=SingletonABCMeta):
    """
    Start all provider services.
    - Rest API
    - Stomp
    - MQTT
    """

    def __init__(self):
        self.rest_api: RestAPI = RestAPI()

    def start_all(self):
        self.__start_mqtt()
        self.__start_stomp()
        self.__start_rest_api()

    def __start_mqtt(self):
        logging.info("Starting MQTT")
        self.mqtt = MQTTProvider()

    def __start_stomp(self):
        logging.info("Starting STOMP")
        self.stomp = STOMPProvider()

    def __start_rest_api(self):
        logging.info("Starting REST API")
        self.rest_api.run()

    def close(self):
        self.mqtt.close()
        self.stomp.close()

    def rest(self):
        """
        Return the REST API instance.
        """
        return self.rest_api

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
