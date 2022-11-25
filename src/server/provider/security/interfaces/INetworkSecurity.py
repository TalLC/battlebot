from abc import ABC, abstractmethod
from threading import Event
from common.Singleton import SingletonABCMeta
from common.config import CONFIG_NETWORK_SECURITY
from provider.security.BannedIP import BannedIP
from provider.security.IPLog import IPLog


class INetworkSecurity(ABC, metaclass=SingletonABCMeta):
    """
    Handle IP ban and unban.
    """
    _BANNED_IPS_FILE_PATH = CONFIG_NETWORK_SECURITY.banned_ips_file_path
    _BANNED_IPS: dict[str, dict[str, BannedIP]] = dict()
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
    def get_ban_info_for_ip(self, host: str, source: str) -> None | BannedIP:
        """
        Fetch the BannedIP object for a given host and source.
        """
        raise NotImplementedError()

    @abstractmethod
    def ban_ip(self, host: str, source: str, reason: str, definitive: bool = False) -> BannedIP:
        """
        Add an entry in _BANNED_IPS and updates the json file.
        Returns the BannedIP object.
        """
        raise NotImplementedError()

    @abstractmethod
    def unban_ip(self, host: str, source: str):
        """
        Remove the banned IP from _BANNED_IPS and updates the json file.
        """
        raise NotImplementedError()

    @abstractmethod
    def update_ip(self, host: str, source: str) -> None | BannedIP:
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
        Read the json ban file and insert BannedIP objects into _BANNED_IPS.
        """
        raise NotImplementedError()

    @abstractmethod
    def _write_ban_file(self):
        """
        Update the json ban file by dumping _BANNED_IPS.
        """
        raise NotImplementedError()
