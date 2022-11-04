from __future__ import annotations

import logging
from abc import ABC
from math import pi
from typing import TYPE_CHECKING
from shapely.geometry import Polygon, LineString, Point

from business.gameobjects.entity.bots.equipments.scanner.interfaces.IScanner import IScanner
from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from utils.geometry import Vector2D, Point2D

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel
    from business.gameobjects.tiles.Tile import Tile


class ScannerModel(IScanner, ABC):
    def __init__(self, bot: BotModel, interval: float = 3, distance: int = 3, fov: float = pi / 2,
                 activated: bool = True):

        self._bot = bot

        self._interval = interval
        self._distance = distance

        self._fov = fov
        self._fov_from = Vector2D.from_angle(self._bot.ry).angle_to(Vector2D.from_angle(-self._fov / 2))
        self._fov_to = Vector2D.from_angle(self._bot.ry).angle_to(Vector2D.from_angle(self._fov / 2))
        self._fov_shape = None

        self._activated = activated
        super().__init__()

    def switch(self) -> None:
        self._activated = not self._activated

    def _update_fov_shape(self) -> None:
        half_fov = self._fov / 2
        front_max = Vector2D.from_angle(self._bot.ry).__mul__(self._distance)
        left_max = Vector2D.from_angle(self._bot.ry - half_fov).__mul__(self._distance)
        right_max = Vector2D.from_angle(self._bot.ry + half_fov).__mul__(self._distance)

        vision_cone = Polygon([
            (self._bot.x, self._bot.z),
            (self._bot.x + left_max.x, self._bot.z + left_max.y),
            (self._bot.x + front_max.x, self._bot.z + front_max.y),
            (self._bot.x + right_max.x, self._bot.z + right_max.y)])

        self._fov_shape = vision_cone

    def _get_objects_in_fov(self) -> Tile:
        # for each object in data, test if shape's obj intersect with fov shape
        # add to detected_object_list
        map_matrix = self._bot.bot_manager.game_manager.map.matrix

        for z, line in enumerate(map_matrix):
            for x, cell in enumerate(line):
                if cell.tile_object.shape is None:
                    continue
                if self._fov_shape.intersects(cell.tile_object.shape.poly):
                    # add cells to the list
                    yield cell.tile_object

    def _get_bots_in_fov(self) -> BotModel:
        # get bots locations from game manager
        # for each bot in data, test if shape of bot is in fov shape
        # add to detected_object_list
        for other_bot in self._bot.bot_manager.get_bots():
            if other_bot == self._bot:
                continue

            if self._fov_shape.intersects(other_bot.shape.poly):
                yield other_bot

    def _store_detected_object(self, result, point, cur_angle, obj):
        bot, d_obj = Point2D(x=self._bot.x, y=self._bot.z), Point2D(x=point.x, y=point.y)
        distance_between_self_and_obj = Vector2D.from_points(bot, d_obj).__abs__()

        if distance_between_self_and_obj < result[cur_angle]['distance']:
            return {"name": obj.name, "distance": distance_between_self_and_obj}
        else:
            return result[cur_angle]

    def _get_detected_objs(self):
        detected_objects: list[BotModel | Tile] = list()
        detected_objects += self._get_objects_in_fov()
        detected_objects += self._get_bots_in_fov()

        return detected_objects

    def _create_line(self, angle):
        cu_vec = Vector2D.from_angle(angle).__mul__(self._distance)
        return LineString([(self._bot.x, self._bot.z), (cu_vec.x, cu_vec.y)])

    def _detection(self, res, agl, obj_list):
        res[agl] = {"name": None, "distance": self._distance}
        cu_line = self._create_line(agl)

        # for all obj in fov, check if intersection(angle, objs)
        for o in obj_list:
            object_ring = LineString(list(o.shape.poly.exterior.coords))
            if cu_line.intersects(object_ring):
                intersections = cu_line.intersection(object_ring)
                if isinstance(intersections, Point):
                    res[agl] = self._store_detected_object(res, point=intersections, cur_angle=agl, obj=o)
                else:
                    for i in intersections.geoms:
                        res[agl] = self._store_detected_object(res, point=i, cur_angle=agl, obj=o)
        return res

    def scanning(self) -> list:
        logging.debug("...........................................................................................")
        result_scan = dict()
        final_result = list()

        # get list of objs detected in fov
        self._update_fov_shape()
        detected_obj_list = self._get_detected_objs()

        angle_scan = self._bot.ry - self._fov / 2
        angle_end_scan = self._bot.ry + self._fov / 2
        previous = DetectedObject(name=None, a_from=angle_scan, to=angle_scan, distance=self._distance)

        logging.debug(f"bot heading {self._bot.ry} and looks between : {angle_scan % 2*pi} and {angle_end_scan % 2*pi}")

        # detect data every degree
        while angle_scan < angle_end_scan:
            result_scan = self._detection(result_scan, angle_scan, detected_obj_list)
            angle_scan += pi / 180

        for angle, scan_data in result_scan.items():

            # if scan_data are same as previous, update `to` and `distance` values
            if previous.name == scan_data['name'] \
                    and (previous.distance - 0.5) < scan_data['distance'] < (previous.distance + 0.5):
                previous.to = angle
                previous.distance = (previous.distance + scan_data['distance'])/2
                continue

            # append object
            final_result.append(previous)

            # prepare next object
            previous = DetectedObject(name=scan_data['name'], a_from=angle, to=angle, distance=scan_data['distance'])

        # append last object
        final_result.append(previous)

        # for debug
        for e in final_result:
            logging.debug(f"from {e.a_from % 2*pi} to {e.to % 2*pi}, name : {e.name}, distance : {e.distance}")

        return final_result
