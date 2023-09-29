from __future__ import annotations
from typing import TYPE_CHECKING
import math
from random import Random

from business.interfaces.IPluginSpawn import IPluginSpawn

if TYPE_CHECKING:
    from business.maps.Map import Map


class RandomSpawn(IPluginSpawn):

    def __init__(self, game_map: Map):
        super().__init__(game_map)

    def process(self, team_id) -> tuple:
        """
        Returns a random spawnable position.
        """
        rand = Random()
        max_x = self.game_map.width - 4
        max_z = self.game_map.height - 4
        min_x = 3
        min_z = 3
        spawn_x = rand.randint(min_x, max_x)
        spawn_z = rand.randint(min_z, max_z)
        spawn_ry = Random().randint(0, math.floor(2 * math.pi * 100)) / 100

        while not self.game_map.is_walkable_at(spawn_x, spawn_z) \
                or len(self.game_map.map_manager.game_manager.bot_manager.get_bots_in_radius(
            origin=(spawn_x, spawn_z),
            radius=max_x / self.game_map.map_manager.game_manager.max_players
        )
        ):
            spawn_x = rand.randint(min_x, max_x)
            spawn_z = rand.randint(min_z, max_z)

        return spawn_x, spawn_z, spawn_ry

    def required(self) -> bool:
        """
        Verification for usage method of spawn.
        """
        return True
