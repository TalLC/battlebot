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
    _map_id: str
    _height: int
    _width: int
    _data: list
    _matrix: list

    @property
    def infos(self):
        return {
                "id": self._map_id,
                "height": self._height,
                "width": self._width,
                "data": self._data
            }

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def matrix(self):
        return self._matrix

    @property
    def data(self):
        return self._data

    def __init__(self):
        self._data = []
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

            self._map_id = map_id
            self._height = save_map['height']
            self._width = save_map['width']
            self._data = save_map['data']
            self._matrix = self.load()

        else:
            logging.error(f"La map {map_id} n'a pas été trouvée.")

    def load(self) -> list:
        """
            Génère la matrice du terrain.
        """
        # On créé un tableau vide aux dimensions de la map
        mat = []
        for h in range(self._height):
            current_line = []
            for w in range(self._width):
                current_line.append(None)
            mat.append(current_line)

        # On créé un obj Tile pour chaque cellule de la map
        for d in self._data:
            mat[d['x']][d['z']] = TileFactory.create_tile(tile_type=d['tile'], x=d['x'], z=d['z'],
                                                          tile_object=TileObjectFactory.create_tileobject(
                                                              d['tile_object'], d['x'], d['z']))
        return mat


if __name__ == '__main__':
    mymap = Map()
    mymap.initialize('empty_3_3')
    print(mymap.infos)
    for r in mymap.matrix:
        for c in r:
            print(c)
