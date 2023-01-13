from __future__ import annotations

from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.equipments.scanner.models.ScannerModel import ScannerModel

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class SimpleScanner(ScannerModel):
    _name = "Simple scanner"
    _interval = 1.0
    _distance = 10
    _fov = 90.0

    def __init__(self, bot: BotModel):
        super().__init__(bot=bot, name=self._name, interval=self._interval, distance=self._distance,
                         fov=self._fov, activated=True)
