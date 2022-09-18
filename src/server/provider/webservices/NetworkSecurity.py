import json
import logging
from time import sleep
from fastapi import WebSocket
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread, Event
from common.Singleton import SingletonABCMeta
from common.config import DATETIME_STR_FORMAT
from provider.webservices.BlacklistedIP import BlacklistedIP
from provider.webservices.IPLog import IPLog

BAN_REASON_TOO_MANY_CONNECTIONS = "Too many connections in a short delay"


class NetworkSecurity(metaclass=SingletonABCMeta):
    """
    Automatically ban IP address that spams a service.
    """
    _MAX_CONNECTIONS_IN_DELAY = 10
    _CONNECTIONS_DELAY_FOR_ONE_IP = timedelta(minutes=1)
    _CONNECTION_DELAY_BEFORE_DEBAN = timedelta(minutes=5)

    _BLACKLISTED_IPS_FILE_PATH = Path('conf', 'blacklisted_ips.json')
    _BLACKLISTED_IPS: dict[str, BlacklistedIP] = dict()
    _IP_CONNECTION_LOGS: dict[int, IPLog] = dict()

    def __init__(self):
        self._BLACKLISTED_IPS = self.read_blacklist_file()
        self._thread_event = Event()
        self._thread = Thread(target=self._thread_deban_check, args=(self._thread_event,)).start()

    def stop_thread(self):
        self._thread_event.set()

    def _thread_deban_check(self, e: Event):
        while not e.is_set():
            for host, blacklisted in self._BLACKLISTED_IPS.copy().items():
                if datetime.now() - blacklisted.timestamp > self._CONNECTION_DELAY_BEFORE_DEBAN:
                    self.unban_ip(host)
            sleep(10)

    def update_ip(self, host: str, source: str) -> None | BlacklistedIP:
        # Check if the IP is not already banned
        if not self.is_ip_allowed(host, source):
            return self.get_ban_info_for_ip(host, source)

        # IP is not banned, adding a connection log
        index = len(self._IP_CONNECTION_LOGS.keys()) + 1
        self._IP_CONNECTION_LOGS[index] = IPLog(host, datetime.now(), source)

        # Check if this IP made too many connections
        if len([found for found in self._IP_CONNECTION_LOGS.values() if found.host == host]) > 0:
            # Fetching logs for this source that are in the maximum delay
            host_logs = self._get_logs_in_delay(host, source)

            # Check if this host has exceeded its maximum connections count for this source
            if len(host_logs) > self._MAX_CONNECTIONS_IN_DELAY:
                return self.ban_ip(host, source, BAN_REASON_TOO_MANY_CONNECTIONS)

        return None

    def is_ip_allowed(self, host: str, source: str) -> bool:
        if host in self._BLACKLISTED_IPS.keys():
            blacklisted = self._BLACKLISTED_IPS[host]
            if blacklisted.source == source:
                return False
        return True

    def get_ban_info_for_ip(self, host: str, source: str) -> None | BlacklistedIP:
        if host in self._BLACKLISTED_IPS.keys():
            blacklisted = self._BLACKLISTED_IPS[host]
            if blacklisted.source == source:
                return self._BLACKLISTED_IPS[host]
        return None

    def ban_ip(self, host: str, source: str, reason: str, definitive: bool = False) -> BlacklistedIP:
        timestamp = datetime.now().strftime(DATETIME_STR_FORMAT)
        blacklisted = BlacklistedIP(host, timestamp, source, reason, definitive)
        self._BLACKLISTED_IPS[host] = blacklisted
        self._update_ban_file()
        return blacklisted

    def unban_ip(self, host: str):
        logging.debug(f"Unbanning {host}")
        self._BLACKLISTED_IPS.pop(host)
        self._update_ban_file()

    def _get_logs_in_delay(self, host: str, source: str) -> [IPLog]:
        # Fetch previous connections from this host and from this source
        # and that are less than self._CONNECTIONS_DELAY_FOR_ONE_IP old
        previous_connections = [
            found for found in list(self._IP_CONNECTION_LOGS.values())
            if found.host == host
            and found.source == source
            and datetime.now() - found.timestamp <= self._CONNECTIONS_DELAY_FOR_ONE_IP
        ]

        # Sort the list from the first log top the latest
        previous_connections.sort(key=lambda x: x.timestamp)

        return previous_connections

    def _update_ban_file(self):
        """
        Update the json blacklist file.
        """
        data = dict()
        for key, value in self._BLACKLISTED_IPS.items():
            data[key] = value.json()

        self._BLACKLISTED_IPS_FILE_PATH.write_text(json.dumps(data))

    def read_blacklist_file(self):
        file_data = json.loads(self._BLACKLISTED_IPS_FILE_PATH.read_text())
        data = dict()
        for key, value in file_data.items():
            data[key] = BlacklistedIP(**value)
        return data


def antispam_websocket(func):
    async def wrap(websocket: WebSocket):
        blacklisted = NetworkSecurity().update_ip(websocket.client.host, 'websocket')
        await websocket.accept()

        if blacklisted is None:
            await func(websocket)
        else:
            await websocket.send_json(blacklisted.light_json())
            await websocket.close()

    return wrap
