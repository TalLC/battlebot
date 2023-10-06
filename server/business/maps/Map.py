from __future__ import annotations
import logging
from typing import TYPE_CHECKING, List

from business.gameobjects.tiles.TileFactory import TileFactory
from business.maps.TilesGrid import TilesGrid
from business.maps.MapSpawner import MapSpawner

if TYPE_CHECKING:
    from business.MapManager import MapManager
    from business.gameobjects.tiles.Tile import Tile


class Map:

    DEFAULT_PREVIEW = "/9j/7gAOQWRvYmUAZEAAAAAB/9sAhAABAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAgICAgICAgICAgIDAwMDAwMDAwMDAQEBAQEBAQEBAQECAgECAgMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwP/wAARCAAQABADAREAAhEBAxEB/90ABAAC/8QAYwABAQAAAAAAAAAAAAAAAAAAAAkBAQEBAQAAAAAAAAAAAAAAAAAFBgcQAAIDAQEBAQAAAAAAAAAAAAYHAwQFCAIJAREAAgICAgIDAQAAAAAAAAAAAgMBBBEFEwYSByFBIxT/2gAMAwEAAhEDEQA/AJF989t9FHfT3YEQL2L0vz0XJZyusBrL8ab7ECuezMYTpUQDgjEF6OEf5lFdNvdABCT3Ng2MySgUbGbZtVdGPT1IMn1W5evXFpqBbGpvxrmfEU5XYFWJIwMjkluKJn85GVmQzxkEkKo5pFH3R1bYbHsNrrr+yem7O6q1v70Lgb2ldsJYKq9qsmsCLmsU0AiLwOC7UruibyLKq7tkTgbtvooE6e4/iOuxel+hS50uVKANlfkrfYhrz2GDDiKh8cLojTR3T/TosVt4QAXx+4cGvmR0BfY0q1q1oyaeXPk+XL16mt1Q7Y29+VcD4hnC64tzImZicExwxEfnAwsCKOQjkSVKaPujtOw13YavXX9b9N1t1arf3vXBXt07XysW16tZ1Y0U9Y1pnE3jcd23XTM0UVlWE7If/9CV/wBG/l8zsLv/AKrP6SF6ybqYPSLy6wCik18RHZE0C5yx2iI4ya7IDVgcL9Ujq7aFncjmg3qM5J+ZMObHBn3otD1tQUdcnUyT7W1afisMAtfw1kl9QwgMFgOIIyKCKcCIgWZIMN3fZ+yFp1Oh9da+rD71mCsXbs8lCgpEZ5G0lWqtu9acLDTUSliVL8nOsW0isEW3zk+XzO3e/wDlQ/uoXrJRJgCIvTrP6LsXxECESvLk1HVIgfJsMgyWAOv2sOsRoVsOOGDBowEn7kzaUc+fRiz/ADtTtinUwSLWqafiwMGtny1cj9SwQAGAWZICGBKMkJAOII3SNn7IYnbaH2Lr6svo2ZKvdpTx0L6nxnkVSbatW6NpIrBNtLmOUzxS6vbcLDRU/9k="

    @property
    def infos(self):
        """
        Returns all map information.
        """
        map_metadata = self.metadata
        map_metadata |= {
            "data": self._tiles_grid.json()
        }
        return map_metadata

    @property
    def metadata(self):
        """
        Returns map metadata.
        """
        return {
            "id": self.id,
            "name": self.name,
            "preview": self.preview,
            "height": self.height,
            "width": self.width,
            "environment": self.environment,
            "spawners": len(self.spawners)
        }

    @property
    def map_manager(self) -> MapManager:
        return self._map_manager

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def preview(self) -> str:
        return self._preview

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def spawners(self) -> List[MapSpawner]:
        return self._spawners

    @property
    def tiles_grid(self) -> TilesGrid:
        return self._tiles_grid

    def __init__(self, map_manager: MapManager, map_id: str):
        self._map_manager = map_manager

        if self.map_manager.does_map_exists(map_id=map_id):
            saved_map = self.map_manager.read_map_data(map_id)
            self._id = map_id
            self._name = saved_map['name']
            self._preview = saved_map['preview'] if 'preview' in saved_map else self.DEFAULT_PREVIEW
            self._width = saved_map['width']
            self._height = saved_map['height']
            self._environment = saved_map['environment'] if 'environment' in saved_map else str()

            spawners = saved_map['spawners'] if 'spawners' in saved_map else None
            if spawners:
                self._spawners = list(
                    [MapSpawner(team_id=s['team'], x=s['x'], z=s['z'], ry=s['ry']) for s in spawners]
                )
            else:
                self._spawners = list()

            self._tiles_grid = TilesGrid(
                self.load(
                    width=self._width,
                    height=self._height,
                    tiles_data=saved_map['tiles']
                )
            )
        else:
            logging.error(f"{map_id} is not a valid map id.")

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


if __name__ == '__main__':
    from business.GameManager import GameManager
    my_map = Map(MapManager(GameManager()), "empty_3_3")
    print(my_map.infos)
    for r in my_map.tiles_grid.json():
        for c in r:
            print(c)
