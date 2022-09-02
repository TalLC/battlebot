import uuid


class ClientConnection:
    """
    Ensure that the client is able to read from Rest, STOMP and MQTT.
    """

    @property
    def bot_id(self) -> str:
        return self._bot_id

    @property
    def is_connected(self) -> bool:
        """
        Returns True if all the ids have been sent back by the client.
        """
        return self._is_rest_connected and self._is_stomp_connected and self._is_mqtt_connected

    @property
    def source_request_id(self) -> str:
        return self._source_request_id

    @property
    def source_stomp_id(self) -> str:
        return self._source_stomp_id

    @property
    def source_mqtt_id(self) -> str:
        return self._source_mqtt_id

    def __init__(self, bot_id: str):
        self._bot_id = bot_id

        self._source_request_id = str(uuid.uuid4())
        self._is_rest_connected = False

        self._source_stomp_id = str(uuid.uuid4())
        self._is_stomp_connected = False

        self._source_mqtt_id = str(uuid.uuid4())
        self._is_mqtt_connected = False

    def connect(self, request_id: str, stomp_id: str, mqtt_id: str) -> bool:
        """
        Check all ids and return True if all ids are the same as the ones sent by the client.
        """
        if self._source_request_id == request_id:
            self._is_rest_connected = True

        if self._source_stomp_id == stomp_id:
            self._is_stomp_connected = True

        if self._source_mqtt_id == mqtt_id:
            self._is_mqtt_connected = True

        return self.is_connected
