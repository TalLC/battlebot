from pathlib import Path
from datetime import timedelta
from dataclasses import dataclass


@dataclass
class NetworkSecurityConfig:
    enable_auto_ban: bool
    banned_ips_file: str
    max_connections_in_interval: int
    unban_check_interval_in_seconds: int
    interval_for_max_connections: dict
    delay_before_unban: dict

    @property
    def banned_ips_file_path(self) -> Path:
        return Path(self.banned_ips_file)

    @property
    def interval_for_max_connections_timedelta(self) -> timedelta:
        _dict_interval = self.interval_for_max_connections
        return timedelta(
            hours=_dict_interval['hours'] if 'hours' in _dict_interval else 0,
            minutes=_dict_interval['minutes'] if 'minutes' in _dict_interval else 0,
            seconds=_dict_interval['seconds'] if 'seconds' in _dict_interval else 0
        )

    @property
    def delay_before_unban_timedelta(self) -> timedelta:
        _dict_interval = self.delay_before_unban
        return timedelta(
            hours=_dict_interval['hours'] if 'hours' in _dict_interval else 0,
            minutes=_dict_interval['minutes'] if 'minutes' in _dict_interval else 0,
            seconds=_dict_interval['seconds'] if 'seconds' in _dict_interval else 0
        )
