import math
from random import Random

from business.interfaces.IPluginSpawn import IPluginSpawn


class RandomSpawn(IPluginSpawn):

    def __init__(self, map):
        super().__init__(map)

    def process(self, team_id) -> tuple:
        """
        Returns a random spawnable position.
        """
        rand = Random()
        max_x = self.map.width - 4
        max_z = self.map.height - 4
        min_x = 3
        min_z = 3
        spawn_x = rand.randint(min_x, max_x)
        spawn_z = rand.randint(min_z, max_z)
        spawn_ry = Random().randint(0, math.floor(2 * math.pi * 100)) / 100

        while not self.map.is_walkable_at(spawn_x, spawn_z) \
                or len(self.map.game_manager.bot_manager.get_bots_in_radius(
            origin=(spawn_x, spawn_z),
            radius=max_x / self.map.game_manager.max_players
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