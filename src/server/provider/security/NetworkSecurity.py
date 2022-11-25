import json
import logging
from time import sleep
from datetime import datetime
from threading import Thread, Event
from common.config import CONFIG_NETWORK_SECURITY
from common.config import DATETIME_STR_FORMAT
from provider.security.interfaces.INetworkSecurity import INetworkSecurity
from provider.security.BannedIP import BannedIP
from provider.security.IPLog import IPLog

BAN_REASON_TOO_MANY_CONNECTIONS = "Too many connections in a short delay"


class NetworkSecurity(INetworkSecurity):

    def __init__(self):
        self._BANNED_IPS = self.read_ban_file()
        self._thread_event = Event()
        self._thread = Thread(target=self._thread_unban_check, args=(self._thread_event,)).start()

    def stop_thread(self):
        # Set the event to stop the thread
        self._thread_event.set()

    def _thread_unban_check(self, e: Event):
        # Listening to the event to know when to stop the thread
        while not e.is_set():
            # Browsing BannedIP objects
            # We need to use dict.copy() to avoid issue when iterating dicts while removing keys
            for host, sources in self._BANNED_IPS.copy().items():
                for source, banned_ip in sources.copy().items():
                    # We unban non-definitive bans only
                    if not banned_ip.definitive:
                        # If the ban lasts for more than max delay, we unban
                        delta = datetime.now() - banned_ip.timestamp
                        if delta > CONFIG_NETWORK_SECURITY.delay_before_unban_timedelta:
                            self.unban_ip(host, source)
            # Checking this every x seconds
            sleep(CONFIG_NETWORK_SECURITY.unban_check_interval_in_seconds)

    def is_ip_allowed(self, host: str, source: str) -> bool:
        # Check if host has a ban
        if host in self._BANNED_IPS.keys():
            # Check if the ban concerns the desired source
            if source in self._BANNED_IPS[host]:
                return False
        return True

    def get_ban_info_for_ip(self, host: str, source: str) -> None | BannedIP:
        # Check if host has a ban
        if host in self._BANNED_IPS.keys():
            # Check if the ban concerns the desired source
            if source in self._BANNED_IPS[host]:
                return self._BANNED_IPS[host][source]
        return None

    def ban_ip(self, host: str, source: str, reason: str, definitive: bool = False) -> BannedIP:
        # Get ban hour
        timestamp = datetime.now().strftime(DATETIME_STR_FORMAT)

        # Create the banned ip object
        banned_ip = BannedIP(host, timestamp, source, reason, definitive)

        # Creating entry if first ban for this host
        if host not in self._BANNED_IPS:
            self._BANNED_IPS[host] = dict()

        # Adding a ban for the specified source
        self._BANNED_IPS[host] |= {source: banned_ip}

        # Updating ban file
        self._write_ban_file()
        return banned_ip

    def unban_ip(self, host: str, source: str):
        # Check if host has a ban
        if host in self._BANNED_IPS.keys():
            # Check if the ban concerns the desired source
            if source in self._BANNED_IPS[host]:
                logging.debug(f"[NETWORK_SECURITY] Unbanning {host} for {source}")
                self._BANNED_IPS[host].pop(source)

                # If there is no source left, we remove the entry
                if len(self._BANNED_IPS[host].values()) <= 0:
                    self._BANNED_IPS.pop(host)

                # Updating ban file
                self._write_ban_file()
        else:
            logging.debug(f"[NETWORK_SECURITY] Cannot unban {host} for {source}: not banned")

    def update_ip(self, host: str, source: str) -> None | BannedIP:
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
            if len(host_logs) > CONFIG_NETWORK_SECURITY.max_connections_in_interval:
                return self.ban_ip(host, source, BAN_REASON_TOO_MANY_CONNECTIONS)

        return None

    def get_connections_logs_in_delay(self, host: str, source: str) -> [IPLog]:
        # Fetch previous connections from this host and from this source
        # and that are less than 'interval' old
        previous_connections = [
            found for found in list(self._IP_CONNECTION_LOGS.values())
            if found.host == host
            and found.source == source
            and datetime.now() - found.timestamp <= CONFIG_NETWORK_SECURITY.interval_for_max_connections_timedelta
        ]

        # Sort the list from the first log top the latest
        previous_connections.sort(key=lambda x: x.timestamp)

        return previous_connections

    def read_ban_file(self):
        # Load json file
        file_data = json.loads(self._BANNED_IPS_FILE_PATH.read_text())

        # Convert json into BannedIP object
        data = dict()
        for host, sources in file_data.items():
            for source, banned_ip in sources.items():
                if host not in data:
                    data[host] = dict()
                data[host] |= {source: BannedIP(**banned_ip)}
        return data

    def _write_ban_file(self):
        # Convert BannedIP object into json
        data = dict()
        for host, sources in self._BANNED_IPS.items():
            for source, banned_ip in sources.items():
                if host not in data:
                    data[host] = dict()
                data[host] |= {source: banned_ip.json()}

        # Writing ban file
        self._BANNED_IPS_FILE_PATH.write_text(json.dumps(data))
