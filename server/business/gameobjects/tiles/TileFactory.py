from business.gameobjects.tiles.Ground import Ground
from business.gameobjects.tiles.GroundWater import GroundWater
from business.gameobjects.tiles.Tile import Tile
from business.gameobjects.tiles.Void import Void
from business.gameobjects.tiles.Water import Water
from business.gameobjects.tiles.Desintegrator import Desintegrator


class TileFactory:

    @staticmethod
    def create_tile(tile_type, x, z) -> Tile:
        if tile_type.lower() == "ground":
            return Ground(x=x, z=z)
        elif tile_type.lower() == "groundwater":
            return GroundWater(x=x, z=z)
        elif tile_type.lower() == "water":
            return Water(x=x, z=z)
        elif tile_type.lower() == "void":
            return Void(x=x, z=z)
        elif tile_type.lower() == "desintegrator":
            return Desintegrator(x=x, z=z)
