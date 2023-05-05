import logging
from fastapi import FastAPI
from common.Singleton import SingletonABCMeta
from provider.webservices.RestProvider import RestProvider
from provider.webservices.WebsocketProvider import WebsocketProvider
from provider.webservices.WebsiteProvider import WebsiteProvider
from provider.brokers.MQTTProvider import MQTTProvider
from provider.brokers.STOMPProvider import STOMPProvider


class ProviderManager(metaclass=SingletonABCMeta):
    """
    Start all provider services.
    - Website
    - Websocket
    - Rest
    """

    @property
    def website(self):
        """
        Return the website instance.
        """
        return self.__website

    @property
    def websocket(self):
        """
        Return the websocket instance.
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
        self.__start_website()
        self.__start_websocket()
        self.__start_rest_api()

    def __start_website(self):
        logging.info("[PROVIDER_MANAGER] Starting Website")
        self.__website = WebsiteProvider(self.__app)

    def __start_websocket(self):
        logging.info("[PROVIDER_MANAGER] Starting Websocket")
        self.__websocket = WebsocketProvider(self.__app)

    def __start_rest_api(self):
        logging.info("[PROVIDER_MANAGER] Starting REST API")
        self.__rest_api = RestProvider(self.__app)
