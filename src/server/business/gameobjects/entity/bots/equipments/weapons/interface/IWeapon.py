from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class IWeapon(ABC):

    @property
    def bot(self) -> BotModel:
        """ Owner of this weapon instance """
        raise NotImplementedError()

    @property
    def name(self) -> str:
        """ Name of the weapon """
        raise NotImplementedError()

    @property
    def damages(self) -> int:
        """ Damages dealt by the weapon """
        raise NotImplementedError()

    @property
    def reach_distance(self) -> int:
        """ Range of the weapon """
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()
