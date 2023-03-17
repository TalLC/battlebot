from datetime import datetime
from common.ErrorCode import NETWORK_BANNED_IP_TEMP, NETWORK_BANNED_IP_DEF
from common.config import DATETIME_STR_FORMAT


class BannedIP:

    @property
    def host(self) -> str:
        return self._host

    @property
    def timestamp(self) -> datetime:
        return datetime.strptime(self._timestamp, DATETIME_STR_FORMAT)

    @property
    def timestamp_str(self) -> str:
        return self._timestamp

    @property
    def source(self) -> str:
        return self._source

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def definitive(self) -> bool:
        return self._definitive

    def __init__(self, host: str, timestamp: str, source: str, reason: str, definitive: bool) -> None:
        self._host = host
        self._timestamp = timestamp
        self._source = source
        self._reason = reason
        self._definitive = definitive

    def json(self) -> dict:
        return {
            "host": self.host,
            "timestamp": self.timestamp_str,
            "source": self.source,
            "reason": self.reason,
            "definitive": self.definitive
        }

    def light_json(self) -> dict:
        if self.definitive:
            ban_message = str(NETWORK_BANNED_IP_DEF)
        else:
            ban_message = str(NETWORK_BANNED_IP_TEMP)
        return {
            "action": "ban_ip",
            "timestamp": self.timestamp_str,
            "message": f"{ban_message}. Reason: {self.reason}"
        }
