from __future__ import annotations

import logging
import math
from abc import ABC
from typing import TYPE_CHECKING

from business.gameobjects.entity.bots.equipments.scanner.interfaces.IScanner import IScanner
from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from business.shapes.ShapeFactory import Shape, ShapeFactory
from business.shapes.ShapesUtils import get_nearest_point

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


class ScannerModel(IScanner, ABC):
    def __init__(self, bot: BotModel, interval: float = 3, distance: int = 3, fov: float = 90.0,
                 activated: bool = True):

        self._bot = bot

        self._interval = interval
        self._distance = distance
        self._fov = fov

        self._activated = activated
        super().__init__()

    def switch(self) -> None:
        self._activated = not self._activated

    def _get_fov_angles(self) -> (float, float):

        min_angle = (self._bot.ry_deg - self._fov / 2) % 360
        max_angle = (self._bot.ry_deg + self._fov / 2) % 360

        return min_angle, max_angle

    @staticmethod
    def _keep_nearest_values(r_raw: list[dict]) -> list[dict]:
        r_clean = []
        for d1 in r_raw:
            angles = [x['angle'] for x in r_clean]
            if d1["angle"] not in angles:
                r_clean.append(d1)
            else:
                for d2 in r_clean:
                    if d1["angle"] == d2["angle"]:
                        if d1["distance"] < d2["distance"]:
                            r_clean.remove(d2)
                            r_clean.append(d1)
        return r_clean

    @staticmethod
    def _create_detected_objects(r_raycast):
        list_detected_objects = []
        for i, e in enumerate(r_raycast):
            if i == 0:
                list_detected_objects.append(
                    DetectedObject(name=e['name'], a_from=e['angle'], a_to=e['angle'], distance=e['distance']))
                continue
            previous_obj = list_detected_objects[-1]
            if e['name'] == previous_obj.name:
                if math.isclose(e['distance'], previous_obj.distance, rel_tol=0.5):
                    previous_obj.distance = sum([previous_obj.distance, e['distance']]) / len([previous_obj.distance, e['distance']])
                    previous_obj.a_to = e['angle']
            else:
                list_detected_objects.append(
                    DetectedObject(name=e['name'], a_from=e['angle'], a_to=e['angle'], distance=e['distance']))

        return list_detected_objects

    def _raycastroll(self):

        visu_rcast = list()
        # TODO : récupérer seulement les objets en face du bot.
        detected_objects = self._bot.bot_manager.game_manager.map.get_all_objects_on_map()

        # Get bot's shape
        bot_shape = self._bot.shape

        # Calculate the angles of the field of view
        min_angle, max_angle = self._get_fov_angles()

        result_raycasting = list()
        # Iterate over the angles in the field of view, sending a ray every 1 degree

        start_angle = min_angle

        angle = start_angle

        # while angle != max_angle:
        for i in range(int(self._fov)):
            tmp = "_"
            decimals = angle - int(angle)
            angle = angle % 360 if angle != 360 else 0
            angle += decimals

            # Calculate the end point of the ray
            end_x = self._bot.x + self.distance * math.cos(math.radians(angle))
            end_y = self._bot.z + self.distance * math.sin(math.radians(angle))

            # Create ray
            ray = ShapeFactory().create_shape(shape=Shape.LINE, coords=[(self._bot.x, self._bot.z), (end_x, end_y)])

            # Check each object in the list
            for obj in detected_objects:
                # Get shape of the object
                object_circle = obj.shape

                # Check if ray touch object's shape
                if object_circle.intersects(ray) and object_circle.distance(bot_shape.centroid) > obj.radius:
                    # List the intersections points
                    points_list = object_circle.intersection(ray).boundary

                    nearest_point = get_nearest_point(bot_shape.centroid, points_list)

                    result_raycasting.append({
                        "distance": nearest_point.distance(bot_shape.centroid),
                        "name": obj.name,
                        "angle": angle
                    })
                    tmp = obj.name[0]

            visu_rcast.append(tmp)
            angle += 1

        logging.info(''.join(visu_rcast))
        logging.info(self._create_detected_objects(self._keep_nearest_values(result_raycasting)))

        return self._keep_nearest_values(result_raycasting)

    def scanning(self) -> list:
        # supra magic power +++ infinite mega racasting the revange of the return !
        logging.info(".....................................................................")
        rayc_result = self._raycastroll()

        return self._create_detected_objects(rayc_result)
