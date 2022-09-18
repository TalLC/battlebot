# import json
# import logging
#
# from fastapi import WebSocket
# from datetime import datetime, timedelta
# from pathlib import Path
# from common.Singleton import SingletonABCMeta
# from common.config import DATETIME_STR_FORMAT
# from provider.webservices.BlacklistedIP import BlacklistedIP
# from provider.webservices.IPLog import IPLog
#
#
# class NetworkSecurity(metaclass=SingletonABCMeta):
#     """
#     Automatically ban IP address that spams a service.
#     """
#     _MAX_CONNECTIONS_IN_DELAY = 10
#     _CONNECTIONS_DELAY_FOR_ONE_IP = timedelta(minutes=1)
#     _CONNECTION_DELAY_BEFORE_DEBAN = timedelta(minutes=5)
#
#     _BLACKLISTED_IPS_FILE_PATH = Path('conf', 'blacklisted_ips.json')
#     _BLACKLISTED_IPS: dict[str, BlacklistedIP] = json.loads(_BLACKLISTED_IPS_FILE_PATH.read_text())
#     _IP_CONNECTION_LOGS: dict[int, IPLog] = dict()
#
#     def __init__(self):
#         # deban loop
#         pass
#
#     def update_ip(self, host: str, source: str) -> None | BlacklistedIP:
#         print(f"{host} ({source})")
#         if host in self._IP_CONNECTION_LOGS.keys():
#             if not self.is_ip_allowed(host, source):
#                 # Fetching logs for this source that are in the maximum delay
#                 host_logs = self._get_logs_in_delay(host, source)
#
#                 # Check if this host has exceeded its maximum connections count for this source
#                 if len(host_logs) > self._MAX_CONNECTIONS_IN_DELAY:
#                     return self.ban_ip(host, source, "Too much connections in a short delay")
#             else:
#                 return self.get_ban_info_for_ip(host, source)
#         else:
#             # New log
#             index = len(self._IP_CONNECTION_LOGS.keys()) + 1
#             self._IP_CONNECTION_LOGS[index] = IPLog(host, datetime.now(), source)
#
#         return None
#
#     def is_ip_allowed(self, host: str, source: str) -> bool:
#         if host in self._BLACKLISTED_IPS.keys():
#             blacklisted = self._BLACKLISTED_IPS[host]
#             if blacklisted.source == source:
#                 return False
#         return True
#
#     def get_ban_info_for_ip(self, host: str, source: str) -> None | BlacklistedIP:
#         if host in self._BLACKLISTED_IPS.keys():
#             blacklisted = self._BLACKLISTED_IPS[host]
#             if blacklisted.source == source:
#                 return self._BLACKLISTED_IPS[host]
#         return None
#
#     def ban_ip(self, host: str, source: str, reason: str, definitive: bool = False) -> BlacklistedIP:
#         timestamp = datetime.now().strftime(DATETIME_STR_FORMAT)
#         blacklisted = BlacklistedIP(host, timestamp, source, reason, definitive)
#         self._BLACKLISTED_IPS[host] = blacklisted
#         self._update_ban_file()
#         return blacklisted
#
#     def unban_ip(self, host: str):
#         self._BLACKLISTED_IPS.pop(host)
#         self._update_ban_file()
#
#     def _get_logs_in_delay(self, host: str, source: str) -> [IPLog]:
#         # Fetch previous connections from this host and from this source
#         # and that are less than self._CONNECTIONS_DELAY_FOR_ONE_IP old
#         previous_connections = [
#             found for found in list(self._IP_CONNECTION_LOGS.values())
#             if found.host == host
#             and found.source == source
#             and datetime.now() - found.timestamp <= self._CONNECTIONS_DELAY_FOR_ONE_IP
#         ]
#
#         # Sort the list from the first log top the latest
#         previous_connections.sort(key=lambda x: x.timestamp)
#
#         return previous_connections
#
#     def _update_ban_file(self):
#         """
#         Update the json blacklist file.
#         """
#         self._BLACKLISTED_IPS_FILE_PATH.write_text(json.dumps(self._BLACKLISTED_IPS))
#
#
# def antispam_websocket(func):
#
#     def wrap(websocket: WebSocket):
#         print(websocket.client.host)
#         blacklisted = NetworkSecurity().update_ip(websocket.client.host, 'websocket')
#         print(blacklisted)
#         if blacklisted is None:
#             result = func(websocket)
#             return result
#         else:
#             if blacklisted.definitive:
#                 return f"You are DEFINITIVELY banned from using this service. Reason: {blacklisted.reason}"
#             else:
#                 return f"You are temporary banned from using this service. Reason: {blacklisted.reason}"
#     return wrap
