from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.equipments.scanner.models.ScannerModel import ScannerModel

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class SimpleScanner(ScannerModel, ABC):

    @property
    def interval(self) -> float:
        return self._interval

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def fov(self) -> float:
        return self._fov

    @property
    def activated(self) -> bool:
        return self._activated

    def __init__(self, bot: BotModel):
        self.bot = bot
        super().__init__(self.bot, interval=1.0, distance=10, fov=90.0, activated=True)
