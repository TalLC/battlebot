import json
import logging
from pathlib import Path

from common.Singleton import SingletonABCMeta
from business.gameobjects.tiles.TileFactory import TileFactory
from business.gameobjects.tiles.objects.TileObjectFactory import TileObjectFactory


def list_save_map() -> list:
    """
    Liste les fichiers JSON (donc les maps) stockées.
    """
    maps_dir = Path('data', 'maps')
    maps_list = []

    for save_map in maps_dir.iterdir():
        if save_map.is_file() and save_map.name.endswith('.json'):
            maps_list.append(save_map)

    return maps_list


class Map(metaclass=SingletonABCMeta):
    _id: str
    _height: int
    _width: int
    _tiles: list
    _matrix: list

    @property
    def infos(self):
        return {
            "id": self._id,
            "height": self._height,
            "width": self._width,
            "data": self._tiles
        }

    @property
    def id(self) -> str:
        return self._id

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def matrix(self) -> [[]]:
        return self._matrix

    @property
    def tiles(self) -> list:
        return self._tiles

    def __init__(self):
        self._tiles = []
        self._matrix = []

        self.initialize('empty_9_9')

    @staticmethod
    def does_map_exists(map_id: str) -> bool:
        """
        Vérifie qu'une map correspond à l'id donné.

        :param map_id: identifiant à tester
        """
        maps_list = list_save_map()

        for sm in maps_list:
            if map_id in sm.name:
                return True

        return False

    def initialize(self, map_id: str) -> None:
        """
        Charge les données du terrain depuis le json de sauvegarde.

        :param map_id: identifiant de la map à charger
        """
        if self.does_map_exists(map_id=map_id):
            save_map = json.loads(Path('data', 'maps', f'{map_id}.json').read_text())

            self._id = map_id
            self._height = save_map['height']
            self._width = save_map['width']
            self._tiles = save_map['tiles']
            self._matrix = self.load()

        else:
            logging.error(f"La map {map_id} n'a pas été trouvée.")

    def load(self) -> list:
        """
        Génère la matrice du terrain.
        """
        # On crée un tableau vide aux dimensions de la map
        mat = []
        for h in range(self._height):
            current_line = []
            for w in range(self._width):
                current_line.append(None)
            mat.append(current_line)

        # On crée un obj Tile pour chaque cellule de la map
        for d in self._tiles:
            mat[d['x']][d['z']] = TileFactory.create_tile(
                tile_type=d['tile'], x=d['x'], z=d['z'], tile_object=TileObjectFactory.create_tileobject(
                    d['tile_object'], d['x'], d['z'])
            )
        return mat


if __name__ == '__main__':
    mymap = Map()
    mymap.initialize('empty_3_3')
    print(mymap.infos)
    for r in mymap.matrix:
        for c in r:
            print(c)
