from business.gameobjects.entity.bots.equipments.scanner.interfaces.IScanner import IScanner
from business.gameobjects.entity.bots.equipments.weapons.interface.IWeapon import IWeapon


class Equipment:

    @property
    def scanner(self) -> IScanner:
        return self._scanner

    @property
    def weapon(self) -> IWeapon:
        return self._weapon

    def __init__(self, scanner: IScanner | None = None, weapon: IWeapon | None = None):
        # Creating a scanner to get environmental information
        self._scanner = scanner

        # Weapon to shoot the enemy
        self._weapon = weapon

    def json(self) -> dict:
        return {
            "scanner": self.scanner.json(),
            "weapon": self.weapon.json()
        }
