import logging
import json
from time import sleep
from paho.mqtt import client as mqtt_client
from provider.brokers.config.MQTTConfig import MQTTConfig


class MQTT:
    MQTTMessage = mqtt_client.MQTTMessage

    @property
    def is_connected(self) -> bool:
        """
        Is set to True when the client is connected to the broker.
        """
        return self.__connected

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port

    @property
    def destination_root(self) -> str:
        return self.__destination_root

    def __init__(self):
        self.__connected = False
        self.__host = MQTTConfig.host
        self.__port = MQTTConfig.port
        self.__destination_root = MQTTConfig.destination_root
        self.__connect_timeout = MQTTConfig.connect_timeout

        # MQTT client
        self.__client = mqtt_client.Client()

        # Callback functions
        self.__client.on_connect = self.on_connect
        self.__client.on_publish = self.on_publish

        # Connecting client
        self.__client.username_pw_set(username=MQTTConfig.username, password=MQTTConfig.password)
        self.__client.connect(self.__host, self.__port)

        # Waiting for connection to complete
        timeout = self.__connect_timeout
        while not self.__client.is_connected and timeout > 0:
            sleep(1)
            timeout -= 1

        # Check if connection is successful
        if not self.__client.is_connected:
            raise Exception("Failed to connect to MQTT broker")

        # Starting internal thread to handle publish/subscribe operations
        self.__client.loop_start()

    def __del__(self):
        self.close()

    def on_connect(self, _client: mqtt_client, _userdata, _flags: dict, rc: int):
        """
        Callback function when the client is connected to the broker.
        """
        if rc == mqtt_client.CONNACK_ACCEPTED:
            self.__connected = True
            logging.info("Connected to MQTT Broker!")
        else:
            raise f"Failed to connect to MQTT broker, return code {rc}"

    @staticmethod
    def on_publish(_client: mqtt_client, _userdata, mid: int):
        """
        Callback function when a message is published.
        """
        logging.debug(f"Message id {mid} published")

    def on_message(self, func):
        """
        Register a callback function to be called when a message is received.
        """
        self.__client.on_message = func

    def send_message(self, topic: str, message: dict, retain: bool = False):
        """
        Send a message to a topic.
        """
        res = self.__client.publish(topic=topic, payload=json.dumps(message), retain=retain)
        logging.debug(f"Sending message id {res.mid}")

        if res.rc == mqtt_client.MQTT_ERR_SUCCESS:
            logging.debug(f"Sent `{message}` to topic `{topic}`")
        else:
            logging.error(f"Failed to send message to topic {topic}")

    def subscribe(self, destination: str):
        """
        Subscribe to a topic and receive incoming messages.
        """
        self.__client.subscribe(topic=destination)
        logging.info(f"Subscribed to topic {destination}")

    def loop(self):
        """
        Run the MQTT client loop to read messages.
        """
        self.__client.loop()

    def close(self):
        """
        Close the connection to the broker.
        """
        self.__client.loop_stop()
        self.__client.disconnect()
        logging.info("MQTT client disconnected")
