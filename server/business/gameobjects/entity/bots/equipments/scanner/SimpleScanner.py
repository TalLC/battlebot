from __future__ import annotations

from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.equipments.scanner.models.ScannerModel import ScannerModel

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class SimpleScanner(ScannerModel):
    _name: str = "Simple scanner"
    _interval: float = 0.500
    _distance: int = 10
    _fov: float = 90.0
    _precision: float = 1.0

    def __init__(self, bot: BotModel):
        super().__init__(bot=bot, name=self._name, interval=self._interval, distance=self._distance,
                         fov=self._fov, precision=self._precision, activated=True)
