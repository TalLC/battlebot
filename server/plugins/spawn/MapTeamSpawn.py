from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from business.interfaces.IPluginSpawn import IPluginSpawn

if TYPE_CHECKING:
    from business.maps.Map import Map


class MapTeamSpawn(IPluginSpawn):

    def __init__(self, game_map: Map):
        super().__init__(game_map)
        self.teams = dict()
        self.nb_team = 0

    def process(self, team_id: str) -> tuple:
        """
        Returns spawnable position by teams.
        """
        if team_id not in self.teams:
            self.teams[team_id] = self.nb_team + 1
            logging.info(self.teams)
            self.nb_team += 1
        for spawner in self.game_map.spawners:
            logging.info(spawner)
            if spawner.team_id == self.teams[team_id]:
                return spawner.x, spawner.z, spawner.ry

    def required(self) -> bool:
        """
        Verification for usage method of spawn.
        """
        if len(self.game_map.spawners):
            logging.info(self.game_map.spawners)
            return True
        return False
