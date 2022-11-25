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

    def _update_fov_shape(self) -> None:
        """
        Create a Polygon that represents the field of view.
        """
        raise NotImplementedError()

    def _get_objects_in_fov(self) -> Generator[Tile]:
        """
        Return the list of objects detected in field of view.

        :return: List of cells detected in field of view.
        """
        raise NotImplementedError()

    def _get_bots_in_fov(self) -> Generator[BotModel]:
        """
        Return the list of bots detected in field of view.

        :return: List of cells detected in field of view.
        """
        raise NotImplementedError()

    def scanning(self) -> None:
        """
        Update the fov shape and check if obj are inside.
        """
        raise NotImplementedError()
