import json
from pathlib import Path

from common.Singleton import SingletonABCMeta
from business.gameobjects.tiles.TileFactory import TileFactory
from business.gameobjects.tiles.objects.TileObjectFactory import TileObjectFactory

config = json.loads(Path('conf', '../conf/maps.json').read_text())


class Map(metaclass=SingletonABCMeta):
    _id: str
    _name: str
    _height: int
    _width: int
    _size: tuple
    _data: list
    _matrice: list
    _map_load: bool
    # [0[0, 1, 2, 3]]
    # [1[0, 1, 2, 3]]
    # [2[0, 1, 2, 3]]
    # [3[0, 1, 2, 3]]


    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size

    @property
    def infos(self):
        return {
            "id": self._id,
            "name": self._name,
            "height": self._height,
            "width": self._width,
            "size": self._size,
            "data": self._data
        }

    @property
    def map_load(self):
        return self.map_load

    @property
    def matrice(self):
        return self._matrice

    def __init__(self):
        self._data = []
        self._matrice = []

    @staticmethod
    def does_map_exist(map_id):
        """
        Check if map exist in saved maps.
        """
        if map_id in config.keys():
            return True
        return False

    def generate_map(self, id_map):
        if self.does_map_exist(id_map):
            self._id = id_map
            self.load_map(self._id)
        else:
            self.create_empty_map(4, 4)

    def load_map(self, id_map):
        """
        Load an existing map from id
        """
        if id_map in config.keys():
            self._name = config[id_map]['name']
            self._height = config[id_map]['height']
            self._width = config[id_map]['width']
            self._size = (self._height, self._width)
            self._data = config[id_map]['data']

            for h in range(self._height):
                current_line = []
                for w in range(self._width):
                    current_line.append(None)
                self._matrice.append(current_line)

            for d in self._data:
                print(d)
                self._matrice[d['x']][d['z']] = TileFactory.create_tile(tile_type=d['tile'],
                                                                        x=d['x'],
                                                                        z=d['z'],
                                                                        tile_object=TileObjectFactory.create_tileobject(d['tile_object'], d['x'], d['z']))

            print(self._matrice)

    def set_size_map(self):
        self._size = (self._height, self._width)

    def create_empty_map(self, height, width):
        self._name = "New map"
        self._id = "999"
        self._height = height
        self._width = width
        self.set_size_map()

        for h in range(self._height):
            for w in range(self._width):
                self._data.append(
                    {
                        'tile': 'ground',
                        'tile_object': 'air',
                        'x': h,
                        'y': w
                    }
                )
