from business.gameobjects.tiles.objects.Air import Air
from business.gameobjects.tiles.objects.Rock import Rock
from business.gameobjects.tiles.objects.Tree import Tree
from business.gameobjects.tiles.objects.Wall import Wall


class TileObjectFactory:

    @staticmethod
    def create_tileobject(tile_object: str, x, z):
        if tile_object.lower() == "air":
            return Air(x=x, z=z)
        elif tile_object.lower() == "rock":
            return Rock(x=x, z=z)
        elif tile_object.lower() == "tree":
            return Tree(x=x, z=z)
        elif tile_object.lower() == "wall":
            return Wall(x=x, z=z)
