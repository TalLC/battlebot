from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from business.gameobjects.tiles.TileFactory import TileFactory
from business.gameobjects.tiles.objects.TileObjectFactory import TileObjectFactory

if TYPE_CHECKING:
    from business.GameManager import GameManager
    from business.gameobjects.tiles.Tile import Tile


class Map:
    _id: str
    _height: int
    _width: int
    _tiles: list
    _matrix: [[Tile]]

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
    def matrix(self) -> [[Tile]]:
        return self._matrix

    @property
    def tiles(self) -> list:
        return self._tiles

    def __init__(self, game_object: GameManager, map_id: str):
        self._game_object = game_object
        self._tiles = []

        self.initialize(map_id)

    def does_map_exists(self, map_id: str) -> bool:
        """
        Vérifie qu'une map correspond à l'id donné.

        :param map_id: identifiant à tester
        """
        maps_list = self.list_saved_map()

        for sm in maps_list:
            if map_id in sm.name:
                return True

        return False

    def is_walkable_at(self, x: float, z: float) -> bool:

        if x >= self.width or z >= self.height:
            return False

        if x < 0 or z < 0:
            return False

        cell = self._matrix[int(x)][int(z)]

        return cell.is_walkable

    @staticmethod
    def list_saved_map() -> list:
        """
        Liste les fichiers JSON (donc les maps) stockées.
        """
        maps_dir = Path('data', 'maps')
        maps_list = []

        for save_map in maps_dir.iterdir():
            if save_map.is_file() and save_map.name.endswith('.json'):
                maps_list.append(save_map)

        return maps_list

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

    def load(self) -> [[Tile]]:
        """
        Génère la matrice du terrain.
        """
        # On crée un tableau vide aux dimensions de la map
        mat: [list[Tile]] = list()
        for h in range(self._height):
            current_line: [Tile] = list()
            for w in range(self._width):
                current_line.append(TileFactory.create_tile(tile_type='void', x=w, z=w))
            mat.append(current_line)

        # On crée un obj Tile pour chaque cellule de la map
        for d in self._tiles:
            x = d['x']
            z = d['z']
            mat[x][z] = TileFactory.create_tile(
                tile_type=d['tile'], x=d['x'], z=d['z'], tile_object=TileObjectFactory.create_tileobject(
                    d['tile_object'], d['x'], d['z'])
            )
        return mat

    def get_all_objects_on_map(self) -> list:
        to_return = []

        for line in self._matrix:
            for cell in line:
                if cell.tile_object.has_collision:
                    to_return.append(cell.tile_object)

        return to_return


if __name__ == '__main__':
    mymap = Map(GameManager(), "empty_3_3")
    print(mymap.infos)
    for r in mymap.matrix:
        for c in r:
            print(c)
