from business.gameobjects.tiles.Ground import Ground
from business.gameobjects.tiles.Void import Void
from business.gameobjects.tiles.Water import Water
from business.gameobjects.tiles.objects.Air import Air


class TileFactory:

    @staticmethod
    def create_tile(tile_type, x, z, tile_object=Air()):
        if tile_type.lower() == "ground":
            return Ground(x=x, z=z, tile_object=tile_object)
        elif tile_type.lower() == "water":
            return Water(x=x, z=z, tile_object=tile_object)
        elif tile_type.lower() == "void":
            return Void(x=x, z=z, tile_object=tile_object)
