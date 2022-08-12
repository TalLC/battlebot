from typing import Any

from business.gameobjects.tiles.objects.special.SpecialTileObject import SpecialTileObject


class BonusHealth(SpecialTileObject):
    NAME: str = "Health bonus"

    def __init__(self):
        super().__init__()

    def callback(self, bot) -> Any:
        """
        Implémenter la fonction qui va heal le joueur
        """
        return None
