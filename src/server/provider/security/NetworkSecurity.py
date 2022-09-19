import json
import logging
from time import sleep
from datetime import datetime
from threading import Thread, Event
from common.config import CONFIG_BLACKLIST
from common.config import DATETIME_STR_FORMAT
from provider.security.interfaces.INetworkSecurity import INetworkSecurity
from provider.security.BlacklistedIP import BlacklistedIP
from provider.security.IPLog import IPLog

BAN_REASON_TOO_MANY_CONNECTIONS = "Too many connections in a short delay"


class NetworkSecurity(INetworkSecurity):

    def __init__(self):
        self._BLACKLISTED_IPS = self.read_ban_file()
        self._thread_event = Event()
        self._thread = Thread(target=self._thread_unban_check, args=(self._thread_event,)).start()

    def stop_thread(self):
        self._thread_event.set()

    def _thread_unban_check(self, e: Event):
        while not e.is_set():
            for host, sources in self._BLACKLISTED_IPS.copy().items():
                for source, blacklisted in sources.copy().items():
                    if not blacklisted.definitive:
                        if datetime.now() - blacklisted.timestamp > CONFIG_BLACKLIST.delay_before_unban_timedelta:
                            self.unban_ip(host, source)
            sleep(10)

    def is_ip_allowed(self, host: str, source: str) -> bool:
        if host in self._BLACKLISTED_IPS.keys():
            if source in self._BLACKLISTED_IPS[host]:
                return False
        return True

    def get_ban_info_for_ip(self, host: str, source: str) -> None | BlacklistedIP:
        if host in self._BLACKLISTED_IPS.keys():
            if source in self._BLACKLISTED_IPS[host]:
                return self._BLACKLISTED_IPS[host][source]
        return None

    def ban_ip(self, host: str, source: str, reason: str, definitive: bool = False) -> BlacklistedIP:
        timestamp = datetime.now().strftime(DATETIME_STR_FORMAT)
        blacklisted = BlacklistedIP(host, timestamp, source, reason, definitive)
        if host not in self._BLACKLISTED_IPS:
            self._BLACKLISTED_IPS[host] = dict()
        self._BLACKLISTED_IPS[host] |= {source: blacklisted}
        self._write_ban_file()
        return blacklisted

    def unban_ip(self, host: str, source: str):
        if host in self._BLACKLISTED_IPS.keys():
            if source in self._BLACKLISTED_IPS[host]:
                logging.debug(f"Unbanning {host} for {source}")
                self._BLACKLISTED_IPS[host].pop(source)

                # If there is no source left, we remove the entry
                if len(self._BLACKLISTED_IPS[host].values()) <= 0:
                    self._BLACKLISTED_IPS.pop(host)

                # Updating blacklist json file
                self._write_ban_file()
        else:
            logging.debug(f"Cannot unban {host} for {source}: not banned")

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
            host_logs = self.get_connections_logs_in_delay(host, source)

            # Check if this host has exceeded its maximum connections count for this source
            if len(host_logs) > CONFIG_BLACKLIST.max_connections_in_interval:
                return self.ban_ip(host, source, BAN_REASON_TOO_MANY_CONNECTIONS)

        return None

    def get_connections_logs_in_delay(self, host: str, source: str) -> [IPLog]:
        # Fetch previous connections from this host and from this source
        # and that are less than 'interval' old
        previous_connections = [
            found for found in list(self._IP_CONNECTION_LOGS.values())
            if found.host == host
            and found.source == source
            and datetime.now() - found.timestamp <= CONFIG_BLACKLIST.interval_for_max_connections_timedelta
        ]

        # Sort the list from the first log top the latest
        previous_connections.sort(key=lambda x: x.timestamp)

        return previous_connections

    def read_ban_file(self):
        file_data = json.loads(self._BLACKLISTED_IPS_FILE_PATH.read_text())
        data = dict()
        for host, sources in file_data.items():
            for source, blacklisted in sources.items():
                if host not in data:
                    data[host] = dict()
                data[host] |= {source: BlacklistedIP(**blacklisted)}
        return data

    def _write_ban_file(self):
        data = dict()
        for host, sources in self._BLACKLISTED_IPS.items():
            for source, blacklisted in sources.items():
                if host not in data:
                    data[host] = dict()
                data[host] |= {source: blacklisted.json()}

        self._BLACKLISTED_IPS_FILE_PATH.write_text(json.dumps(data))
