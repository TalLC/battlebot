from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from abc import ABC

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel
    from business.gameobjects.tiles.Tile import Tile


class IScanner(ABC):

    @property
    def interval(self) -> float:
        """ Interval (in seconds) between two scans. """
        raise NotImplementedError()

    @property
    def distance(self) -> int:
        """ Range of scanner. """
        raise NotImplementedError()

    @property
    def fov(self) -> int:
        """ FOV of scanner in radians. """
        raise NotImplementedError()

    @property
    def activated(self) -> int:
        """ Is scanner is activated ? """
        raise NotImplementedError()

    def switch(self) -> None:
        """
        Switch on/off of scanner.
        """
        raise NotImplementedError()

    def scanning(self) -> None:
        """
        Update the fov shape and check if obj are inside.
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()
