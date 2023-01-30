from business.gameobjects.tiles.objects.TileObject import TileObject


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

    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(name=self._NAME, x=x, z=z, health=self._HEALTH_MAX, has_collision=False)

    def _on_death(self) -> None:
        pass

    def _on_hurt(self) -> None:
        pass
