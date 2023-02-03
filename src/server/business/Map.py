from __future__ import annotations
import json
import logging
from random import Random
from pathlib import Path
from typing import TYPE_CHECKING

from business.shapes.ShapesUtils import ShapesUtils
from business.gameobjects.tiles.TileFactory import TileFactory
from business.gameobjects.tiles.objects.TileObject import TileObject

if TYPE_CHECKING:
    from business.GameManager import GameManager
    from business.gameobjects.tiles.Tile import Tile


class TilesGrid:

    @property
    def tiles(self) -> list[Tile]:
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

    def get_all_tiles(self) -> list[Tile]:
        """
        Get all tile objects from the map.
        """
        return [tile for tile in self.tiles]

    def get_tiles_in_radius(self, origin: tuple = (0.0, 0.0), radius: int = 1) -> list[Tile]:
        """
        Get all tile objects from the map.
        """
        # Filtering on radius
        in_range_tiles = list()
        for tile in self.get_all_tiles():
            if ShapesUtils.get_2d_distance_between(origin, (tile.x, tile.z)) <= radius:
                in_range_tiles.append(tile)

        return in_range_tiles

    def get_all_tiles_objects(self, collision_only: bool = True) -> list[TileObject]:
        """
        Get all tile objects from the map.
        """
        return [tile.tile_object for tile in self.tiles
                if not collision_only or (collision_only and tile.tile_object.has_collision)]

    def get_tiles_objects_in_radius(self, collision_only: bool = True, origin: tuple = (0.0, 0.0), radius: int = 1):
        """
        Get tiles objects in radius from the map
        """
        # Filtering on radius
        in_range_tile_objects = list()
        for tile_object in self.get_all_tiles_objects(collision_only=collision_only):
            if ShapesUtils.get_2d_distance_between(origin, (tile_object.x, tile_object.z)) <= radius:
                in_range_tile_objects.append(tile_object)

        return in_range_tile_objects

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
                "shape_name": tile.shape_name.lower() if tile.shape_name else str(),
                "shape_size": tile.shape_size,
                "object": {
                    "id": tile.tile_object.id,
                    "name": tile.tile_object.name,
                    "x": tile.tile_object.x,
                    "z": tile.tile_object.z,
                    "ry": tile.tile_object.ry,
                    "shape_name": tile.tile_object.shape_name.lower() if tile.tile_object.shape_name else str(),
                    "shape_size": tile.tile_object.shape_size
                }
            })

        return tiles_list

    def json2(self, alive_tile_objects_only: bool = False) -> list[dict]:
        """
        Dumps the tile list in a serializable format.
        """
        tiles_list = list()
        for tile in self.tiles:
            tile_dict = {
                "id": tile.id,
                "name": tile.name,
                "x": tile.x,
                "z": tile.z,
                "shape_name": tile.shape_name.lower() if tile.shape_name else str(),
                "shape_size": tile.shape_size
            }

            if tile.tile_object.is_alive:
                tile_object_dict = {
                    "object": {
                        "id": tile.tile_object.id,
                        "name": tile.tile_object.name,
                        "x": tile.tile_object.x,
                        "z": tile.tile_object.z,
                        "ry": tile.tile_object.ry,
                        "shape_name": tile.tile_object.shape_name.lower() if tile.tile_object.shape_name else str(),
                        "shape_size": tile.tile_object.shape_size
                    }
                }
                tile_dict |= tile_object_dict

            tiles_list.append(tile_dict)

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

        return cell.is_walkable and not cell.tile_object.has_collision

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

        # On crée un tile object pour chaque cellule de la map
        for d in tiles_data:
            x = d['x']
            z = d['z']
            tmp_tile = TileFactory.create_tile(tile_type=d['tile'], x=d['x'], z=d['z'])
            tmp_tile.set_tile_object(tile_object_name=d['tile_object'])
            mat[x][z] = tmp_tile
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
