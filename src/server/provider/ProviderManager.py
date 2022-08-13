import logging
from provider.RestAPI import RestAPI
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

    def __start_rest_api(self):
        logging.info("Starting REST API")
        self.rest_api.run()
