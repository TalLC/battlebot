from abc import ABC, abstractmethod
from threading import Event
from common.Singleton import SingletonABCMeta
from common.config import CONFIG_BLACKLIST
from provider.security.BlacklistedIP import BlacklistedIP
from provider.security.IPLog import IPLog


class INetworkSecurity(ABC, metaclass=SingletonABCMeta):
    """
    Handle IP ban and unban.
    """
    _BLACKLISTED_IPS_FILE_PATH = CONFIG_BLACKLIST.blacklist_file_path
    _BLACKLISTED_IPS: dict[str, dict[str, BlacklistedIP]] = dict()
    _IP_CONNECTION_LOGS: dict[int, IPLog] = dict()

    @abstractmethod
    def stop_thread(self):
        """
        Stop unban checking thread.
        """
        raise NotImplementedError()

    @abstractmethod
    def _thread_unban_check(self, e: Event):
        """
        Threaded function that will check every x seconds if a ban has expired.
        Automatically unban every expired temporary bans.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_ip_allowed(self, host: str, source: str) -> bool:
        """
        Check if the IP is already banned for this source.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_ban_info_for_ip(self, host: str, source: str) -> None | BlacklistedIP:
        """
        Fetch the BlacklistedIP object for a given host and source.
        """
        raise NotImplementedError()

    @abstractmethod
    def ban_ip(self, host: str, source: str, reason: str, definitive: bool = False) -> BlacklistedIP:
        """
        Add an entry in _BLACKLISTED_IPS and updates the json file.
        Returns the BlacklistedIP object.
        """
        raise NotImplementedError()

    @abstractmethod
    def unban_ip(self, host: str, source: str):
        """
        Remove the banned IP from _BLACKLISTED_IPS and updates the json file.
        """
        raise NotImplementedError()

    @abstractmethod
    def update_ip(self, host: str, source: str) -> None | BlacklistedIP:
        """
        Check if this IP needs to be automatically banned.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_connections_logs_in_delay(self, host: str, source: str) -> [IPLog]:
        """
        Fetch all logs for an IP and a source that are less old than "interval".
        """
        raise NotImplementedError()

    @abstractmethod
    def read_ban_file(self):
        """
        Read the blacklist json file and insert BlacklistedIP objects into _BLACKLISTED_IPS.
        """
        raise NotImplementedError()

    @abstractmethod
    def _write_ban_file(self):
        """
        Update the json blacklist file by dumping _BLACKLISTED_IPS.
        """
        raise NotImplementedError()
