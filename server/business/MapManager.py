import json
from pathlib import Path
from typing import List

from business.maps.Map import Map
from business.interfaces.IMapManager import IMapManager
from common.Singleton import SingletonABCMeta


class MapManager(IMapManager, metaclass=SingletonABCMeta):

    def get_map(self, map_id: str) -> Map:
        return Map(self, map_id)

    def get_maps_ids(self) -> List[str]:
        maps_dir = Path('data', 'maps')
        maps_list = []

        for save_map in maps_dir.iterdir():
            if save_map.is_file() and save_map.name.endswith('.json'):
                maps_list.append(save_map.stem)

        return maps_list

    def read_map_data(self, map_id) -> dict:
        """
        Read and return the map data
        """
        return json.loads(Path('data', 'maps', f'{map_id}.json').read_text())

    def does_map_exists(self, map_id: str) -> bool:
        """
        Check if the given id is an existing map
        """
        return map_id in self.get_maps_ids()
