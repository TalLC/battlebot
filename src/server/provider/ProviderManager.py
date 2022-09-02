import logging
from common.Singleton import SingletonABCMeta
from provider.webservices.RestProvider import RestProvider
from provider.webservices.WebsocketProvider import WebsocketProvider
from provider.webservices.WebsiteProvider import WebsiteProvider
from provider.brokers.MQTTProvider import MQTTProvider
from provider.brokers.STOMPProvider import STOMPProvider
from fastapi import FastAPI


class ProviderManager(metaclass=SingletonABCMeta):
    """
    Start all provider services.
    - MQTT
    - Stomp
    - Website
    - Websocket
    - Rest
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
    def website(self):
        """
        Return the REST API instance.
        """
        return self.__website

    @property
    def websocket(self):
        """
        Return the REST API instance.
        """
        return self.__websocket

    @property
    def rest(self):
        """
        Return the REST API instance.
        """
        return self.__rest_api

    def __init__(self, app: FastAPI):
        self.__app = app

    def start_all(self):
        self.__start_mqtt()
        self.__start_stomp()
        self.__start_website()
        self.__start_websocket()
        self.__start_rest_api()

    def __start_mqtt(self):
        logging.info("Starting MQTT")
        self.__mqtt = MQTTProvider()

    def __start_stomp(self):
        logging.info("Starting STOMP")
        self.__stomp = STOMPProvider()

    def __start_website(self):
        logging.info("Starting Website")
        self.__website = WebsiteProvider(self.__app)

    def __start_websocket(self):
        logging.info("Starting Websocket")
        self.__websocket = WebsocketProvider(self.__app)

    def __start_rest_api(self):
        logging.info("Starting REST API")
        self.__rest_api = RestProvider(self.__app)

    def close(self):
        self.__mqtt.close()
        self.__stomp.close()
