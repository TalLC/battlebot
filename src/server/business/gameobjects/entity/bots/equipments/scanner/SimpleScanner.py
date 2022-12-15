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
    _name = "Simple scanner"
    _interval = 1
    _distance = 10
    _fov = pi/2

    def __init__(self, bot: BotModel):
        super().__init__(bot=bot, name=self._name, interval=self._interval, distance=self._distance,
                         fov=self.fov, activated=True)
