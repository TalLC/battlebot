import logging
from provider.RestAPI import RestAPI
from provider.MQTTClient import MQTTClient
from provider.STOMPClient import STOMPClient
from common.Singleton import SingletonABCMeta


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
        self.__start_rest_api()
        self.__start_mqtt()
        self.__start_stomp()

    def __start_rest_api(self):
        logging.info("Starting REST API")
        self.rest_api.run()

    def __start_mqtt(self):
        logging.info("Starting MQTT")
        self.mqtt_client = MQTTClient("localhost", 1883, "system", "manager")

    def __start_stomp(self):
        logging.info("Starting STOMP")
        self.stomp_client = STOMPClient("localhost", 61613, "system", "manager")

    def close(self):
        self.mqtt_client.close()
        self.stomp_client.close()

    def rest(self):
        """
        Return the REST API instance.
        """
        return self.rest_api

    def mqtt(self):
        """
        Return the MQTT client instance.
        """
        return self.mqtt_client

    def stomp(self):
        """
        Return the STOMP client instance.
        """
        return self.stomp_client
