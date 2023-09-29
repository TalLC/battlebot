import logging

from business.interfaces.IPluginSpawn import IPluginSpawn


class MapTeamSpawn(IPluginSpawn):

    def __init__(self, map):
        super().__init__(map)
        self.teams = dict()
        self.nb_team = 0

    def process(self, team_id) -> tuple:
        """
        Returns spawnable position by teams.
        """
        if not team_id in self.teams:
            self.teams[team_id] = self.nb_team + 1
            logging.info(self.teams)
            self.nb_team += 1
        for spawn in self.map.spawners:
            logging.info(spawn)
            if spawn['team'] == self.teams[team_id]:
                return spawn['x'], spawn['z'], spawn['ry']


    def required(self) -> bool:
        """
        Verification for usage method of spawn.
        """
        if self.map.spawners:
            logging.info(self.map.spawners)
            return True
        return False