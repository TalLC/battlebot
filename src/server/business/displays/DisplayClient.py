import uuid
from datetime import datetime, timedelta
import starlette.datastructures
from pathlib import Path
from random import Random


class DisplayClient:
    """
    Holds information about clients that has been connected to the websocket.
    """

    __adjectives_dictionary_path = Path('conf', 'dictionaries', 'english-adjectives.txt').read_text()
    __adjectives = __adjectives_dictionary_path.replace('\r\n', '\n').split('\n')

    __gerunds_dictionary_path = Path('conf', 'dictionaries', 'english-gerunds.txt').read_text()
    __gerunds = __gerunds_dictionary_path.replace('\r\n', '\n').split('\n')

    __nouns_dictionary_path = Path('conf', 'dictionaries', 'english-nouns.txt').read_text()
    __nouns = __nouns_dictionary_path.replace('\r\n', '\n').split('\n')

    class Headers:
        accept_encoding: str
        accept_language: str
        origin: str
        user_agent: str

        def __str__(self) -> str:
            return f"\taccept-encoding = {self.accept_encoding}\n" \
                   f"\taccept-language = {self.accept_language}\n" \
                   f"\torigin = {self.origin}\n" \
                   f"\tuser-agent = {self.user_agent}\n"

        def json(self) -> dict:
            return {
                "accept-encoding": self.accept_encoding,
                "accept-language": self.accept_language,
                "origin": self.origin,
                "user-agent": self.user_agent
            }

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def timestamp_start(self) -> datetime:
        return self._timestamp_start

    @property
    def timestamp_stop(self) -> None | datetime:
        return self._timestamp_stop

    @property
    def timestamp_duration(self) -> timedelta:
        if self.status:
            return datetime.now() - self._timestamp_start
        else:
            return self.timestamp_stop - self.timestamp_start

    @property
    def status(self) -> bool:
        return self._status

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def token(self) -> str:
        return self._token

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def headers(self) -> Headers:
        return self._headers

    def __init__(self, id_num: int, host: str, port: int, websocket_headers: starlette.datastructures.Headers):
        self._id = id_num
        self._name = self.__generate_name(seed=host)
        self._timestamp_start = datetime.now()
        self._timestamp_stop = None
        self._status = True
        self._is_ready = False
        self._token = str(uuid.uuid4())
        self._host = host
        self._port = port
        self._headers = DisplayClient.Headers()
        self._headers.accept_encoding = websocket_headers['accept-encoding'] \
            if 'accept-encoding' in websocket_headers else str()
        self._headers.accept_language = websocket_headers['accept-language'] \
            if 'accept-language' in websocket_headers else str()
        self._headers.origin = websocket_headers['origin'] if 'origin' in websocket_headers else str()
        self._headers.user_agent = websocket_headers['user-agent'] if 'user-agent' in websocket_headers else str()

    def __str__(self):
        timestamp_start = self.timestamp_start.strftime('%d/%m/%Y %H:%M:%S')
        timestamp_stop = self.timestamp_stop.strftime('%d/%m/%Y %H:%M:%S') if self.timestamp_stop is not None else ''
        return f"Id: {self.id}\n" \
               f"Name: {self.name}\n" \
               f"Timestamp start: {timestamp_start}\n" \
               f"Timestamp stop: {timestamp_stop}\n" \
               f"Timestamp duration: {str(self.timestamp_duration)}\n" \
               f"Status: {'connected' if self.status else 'disconnected'}\n" \
               f"Is Ready: {self.is_ready}\n" \
               f"Token: {self.token}\n" \
               f"IP and port: {self.host}:{self.port}\n" \
               f"Headers:\n" \
               f"{str(self.headers)}"

    def json(self) -> dict:
        timestamp_start = self.timestamp_start.strftime('%d/%m/%Y %H:%M:%S')
        timestamp_stop = self.timestamp_stop.strftime('%d/%m/%Y %H:%M:%S') if self.timestamp_stop is not None else ''
        return {
            "id": self.id,
            "name": self.name,
            "timestamp_start": timestamp_start,
            "timestamp_stop": timestamp_stop,
            "timestamp_duration": str(self.timestamp_duration),
            "status": 'connected' if self.status else 'disconnected',
            "is_ready": self.is_ready,
            "token": self.token,
            "host": self.host,
            "port": self.port,
            "headers": self.headers.json()
        }

    def set_ready(self):
        self._is_ready = True

    def set_connection_closed(self):
        self._status = False
        self._timestamp_stop = datetime.now()

    def __generate_name(self, seed: str) -> str:
        r = Random(x=seed)
        adjective = self.__adjectives[r.randrange(0, len(self.__adjectives))]
        gerund = self.__gerunds[r.randrange(0, len(self.__gerunds))]
        noun = self.__nouns[r.randrange(0, len(self.__nouns))]

        return f"{adjective.capitalize()}{gerund.capitalize()}{noun.capitalize()}"
