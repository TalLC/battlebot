from __future__ import annotations

import logging
from math import pi
from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.equipments.scanner.models.ScannerModel import ScannerModel
from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from utils.geometry import Vector2D, Point2D

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class SimpleScanner(ScannerModel):

    @property
    def bot(self) -> BotModel:
        return self._bot

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
        super().__init__(bot, interval=1, distance=10, fov=pi/2, activated=True)
