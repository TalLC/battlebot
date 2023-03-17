from typing import Any

from business.gameobjects.tiles.objects.special.SpecialTileObject import SpecialTileObject


class BonusHealth(SpecialTileObject):
    NAME: str = "Trap (stun)"

    def __init__(self):
        super().__init__()

    def callback(self, bot) -> Any:
        """
        Implémenter la fonction qui va bloquer le joueur
        """
        return None
