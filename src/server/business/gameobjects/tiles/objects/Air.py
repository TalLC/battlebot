from __future__ import annotations
from typing import TYPE_CHECKING
from business.gameobjects.tiles.objects.TileObject import TileObject


if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile


class Air(TileObject):
    _NAME = 'Air'
    _HEALTH_MAX: int = 0

    # Collision Shape
    _shape_name = None
    _shape_size = None

    @property
    def shape_name(self) -> str:
        return self._shape_name

    @property
    def shape_size(self) -> float:
        return self._shape_size

    def __init__(self, parent_tile: Tile, x: float = 0.0, z: float = 0.0):
        super().__init__(
            parent_tile=parent_tile, name=self._NAME, x=x, z=z, health=self._HEALTH_MAX, has_collision=False
        )

    def _on_death(self) -> None:
        pass

    def _on_hurt(self) -> None:
        pass
