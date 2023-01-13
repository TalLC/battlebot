from __future__ import annotations
import json
import logging
from random import Random
from pathlib import Path
from typing import TYPE_CHECKING

from business.gameobjects.tiles.TileFactory import TileFactory
from business.gameobjects.tiles.objects.TileObjectFactory import TileObjectFactory

if TYPE_CHECKING:
    from business.GameManager import GameManager
    from business.gameobjects.tiles.Tile import Tile


class TilesGrid:

    @property
    def tiles(self) -> list:
        return self._tiles

    def __init__(self, tiles_matrix: [[Tile]]):

        self._tiles = list()

        # Creating Tiles and Tile objects
        for row in tiles_matrix:
            for tile in row:
                self._tiles.append(tile)

    def get_tile_at(self, x: int, z: int) -> Tile | None:
        """
        Retrieves the Tile at specified location.
        """
        found_tiles = [tile for tile in self.tiles if tile.x == x and tile.z == z]
        return found_tiles[0] if len(found_tiles) > 0 else None

    def json(self) -> list[dict]:
        """
        Dumps the tile list in a serializable format.
        """
        tiles_list = list()
        for tile in self.tiles:
            tiles_list.append({
                "id": tile.id,
                "name": tile.name,
                "x": tile.x,
                "z": tile.z,
                "object": {
                    "id": tile.tile_object.id,
                    "name": tile.tile_object.name,
                    "x": tile.tile_object.x,
                    "z": tile.tile_object.z,
                    "ry": tile.tile_object.ry
                }
            })
        return tiles_list


class Map:

    @property
    def infos(self):
        return {
            "id": self._id,
            "height": self._height,
            "width": self._width,
            "data": self._tiles_grid.json()
        }

    @property
    def id(self) -> str:
        return self._id

    @property
    def game_manager(self) -> GameManager:
        return self._game_manager

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def tiles_grid(self) -> TilesGrid:
        return self._tiles_grid

    def __init__(self, game_manager: GameManager, map_id: str):
        self._game_manager = game_manager

        if self.does_map_exists(map_id=map_id):
            saved_map = json.loads(Path('data', 'maps', f'{map_id}.json').read_text())
            self._id = map_id
            self._width = saved_map['width']
            self._height = saved_map['height']
            self._tiles_grid = TilesGrid(
                self.load(
                    width=self._width,
                    height=self._height,
                    tiles_data=saved_map['tiles']
                )
            )
        else:
            logging.error(f"{map_id} is not a valid map id.")

    def does_map_exists(self, map_id: str) -> bool:
        """
        Vérifie qu'une map correspond à l'id donné.
        """
        maps_list = self.list_saved_map()

        for sm in maps_list:
            if map_id in sm.name:
                return True

        return False

    def is_walkable_at(self, x: float, z: float) -> bool:
        """
        Return if the tile at x, z is walkable.
        """
        if x >= self.width or z >= self.height:
            return False

        if x < 0 or z < 0:
            return False

        cell = self._tiles_grid.get_tile_at(int(x), int(z))

        return cell.is_walkable

    def get_random_spawn_coordinates(self) -> tuple:
        """
        Returns a random spawnable position.
        """
        rand = Random()
        max_x = self.width - 1
        max_z = self.height - 1
        spawn_x = rand.randint(0, max_x)
        spawn_z = rand.randint(0, max_z)

        while not self.is_walkable_at(spawn_x, spawn_z):
            spawn_x = rand.randint(0, max_x)
            spawn_z = rand.randint(0, max_z)

        return spawn_x, spawn_z

    @staticmethod
    def load(width: int, height: int, tiles_data: list[dict]) -> [[Tile]]:
        """
        Génère la matrice du terrain.
        """
        # On crée un tableau vide aux dimensions de la map
        mat: [list[Tile]] = list()
        for h in range(height):
            current_line: [Tile] = list()
            for w in range(width):
                current_line.append(TileFactory.create_tile(tile_type='void', x=w, z=w))
            mat.append(current_line)

        # On crée un obj Tile pour chaque cellule de la map
        for d in tiles_data:
            x = d['x']
            z = d['z']
            mat[x][z] = TileFactory.create_tile(
                tile_type=d['tile'], x=d['x'], z=d['z'], tile_object=TileObjectFactory.create_tileobject(
                    d['tile_object'], d['x'], d['z'])
            )
        return mat

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


if __name__ == '__main__':
    my_map = Map(GameManager(), "empty_3_3")
    print(my_map.infos)
    for r in my_map.tiles_grid.json():
        for c in r:
            print(c)
