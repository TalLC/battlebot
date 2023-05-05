from __future__ import annotations

import logging
from abc import ABC
from itertools import groupby
from threading import Thread, Event
from time import sleep
from typing import TYPE_CHECKING, List

from common.config import CONFIG_GAME
from business.gameobjects.entity.bots.equipments.scanner.interfaces.IScanner import IScanner
from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from business.shapes.ShapeFactory import Shape, ShapeFactory
from business.shapes.ShapesUtils import ShapesUtils
from business.gameobjects.tiles.Tile import Tile
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.mqtt.BotScannerDetectionMessage import BotScannerDetectionMessage
from consumer.webservices.messages.websocket.DebugBotDetectedObjects import DebugBotDetectedObjects

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel
    from shapely.geometry import LineString


class ScannerModel(IScanner, ABC):

    @property
    def bot(self) -> BotModel:
        return self._bot

    @property
    def name(self) -> str:
        return self._name

    @property
    def interval(self) -> float:
        return self._interval

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def fov(self) -> float:
        return self._fov

    @property
    def precision(self) -> float:
        return self._precision

    @property
    def activated(self) -> bool:
        return self._activated

    def __init__(self, bot: BotModel, name: str, interval: float = 3, distance: int = 3, fov: float = 90.0,
                 precision: float = 0.5, activated: bool = True):

        self._bot = bot
        self._name = name

        self._interval = interval
        self._distance = distance
        self._fov = fov
        self._precision = precision
        self._activated = activated
        super().__init__()  # Todo : besoin de cet appel ?

        # Thread's scanner
        self._thread_scanner = Thread(
            target=self._thread_scanning,
            args=(self.bot.event_stop_threads,)
        ).start()

    def _thread_scanning(self, e: Event):
        # Waiting interval between all increments
        loop_wait_ms = 100
        while not e.is_set():
            if self.bot.bot_manager.game_manager.is_started and self.activated:
                detected_objects = self.scanning()
                if detected_objects:
                    ConsumerManager().mqtt.send_message(
                        BotScannerDetectionMessage(self.bot.id, detected_objects=detected_objects))
                    if CONFIG_GAME.is_debug:
                        ConsumerManager().websocket.send_message(
                            DebugBotDetectedObjects(self.bot.id, detected_objects=detected_objects,
                                                    interval=self.interval)
                        )
                sleep(self.interval)
            else:
                sleep(loop_wait_ms / 1000)

    def switch(self) -> None:
        self._activated = not self._activated

    def _get_fov_angles(self) -> (float, float):

        min_angle = (self._bot.ry_deg - self._fov / 2) % 360
        max_angle = (self._bot.ry_deg + self._fov / 2) % 360

        logging.debug(f"[{self._bot.name}] scanning from {min_angle} to {max_angle} [{self._distance}]")

        return min_angle, max_angle

    @staticmethod
    def _keep_nearest_elements(elements: list[dict]) -> list[dict]:
        """
            Keep only the nearest value of detected objects by angle. (Delete the object or part of object in the
            background)
        """
        foreground_elements = []
        for elem1 in elements:
            angles = [x['angle'] for x in foreground_elements]
            if elem1["angle"] not in angles:
                foreground_elements.append(elem1)
            else:
                for elem2 in foreground_elements:
                    if elem1["angle"] == elem2["angle"]:
                        if elem1["distance"] < elem2["distance"]:
                            foreground_elements.remove(elem2)
                            foreground_elements.append(elem1)
        return foreground_elements

    @staticmethod
    def _create_detected_objects(elements: List[dict]) -> List[DetectedObject]:
        """
            Return list of DetectedObject from raycasting's result.
        """
        def key_func(k):
            return k['obj_id']

        list_detected_obj = list()
        r_raycast = sorted(elements, key=key_func)

        for obj_id, hits_group in groupby(r_raycast, key_func):
            hits_list = list(hits_group)

            list_detected_obj.append(DetectedObject(
                obj_id=obj_id,
                name=hits_list[0]['name'],
                object_type=hits_list[0]['object_type'],
                a_from=min([hit["angle"] for hit in hits_list]),
                a_to=max([hit["angle"] for hit in hits_list]),
                distance=sum([hit["distance"] for hit in hits_list])/len(hits_list),
                origin=hits_list[0]['origin'],
                origin_ry=hits_list[0]['origin_ry']
            ))

        return list_detected_obj

    def _iterate_fov_angle(self, min_angle: float, max_angle: float) -> List[float]:
        """
            Return list of angles in fov.
        """
        angles = list()
        tmp_angle = min_angle
        for i in range(0, int((self._fov/self._precision))):
            if min_angle > max_angle and tmp_angle >= 360:
                tmp_angle = 0.0
            angles.append(tmp_angle)
            tmp_angle += self._precision
        return angles

    def create_ray(self, angle: float) -> LineString:
        """
            Return linestring that represents a ray starting from the bot at an angle "angle"
        """
        # Calculate the end point of the ray
        end_coords = ShapesUtils.get_coordinates_at_distance(
            self._bot.coordinates, self.distance, angle, is_degrees=True
        )
        # Create ray
        return ShapeFactory().create_shape(shape=Shape.LINE, coords=[self._bot.coordinates, end_coords])

    def scanning(self) -> List[DetectedObject]:
        """
            Supra magic power +++ infinite mega racasting the revange of the return !
        """
        obj_in_fov = list()

        detected_objects = self._bot.bot_manager.game_manager.get_map_objects(
            bots=True,                      # Get all the bots
            tiles=True,                     # Get all the tiles
            tile_objects=True,              # Get all the tiles objects
            collision_only=True,            # Restrict Tile objects to the ones with collisions only
            radius=self._distance,
            origin=self._bot.coordinates
        )
        # Calculate the angles of the field of view
        min_angle, max_angle = self._get_fov_angles()
        # Init relative angle from bot
        relative_angle = 0 - (self._fov / 2)

        # Shoot ray every [precision value] degree
        for a in self._iterate_fov_angle(min_angle, max_angle):
            ray = self.create_ray(a)
            # Check if collision between ray and elements on the map.
            for item in detected_objects:
                # Keeping Tiles we cannot walk on
                if isinstance(item, Tile):
                    if item.is_walkable:
                        continue

                if item != self._bot:
                    if item.shape.intersection(ray):
                        # get all intersections points
                        points_list = item.shape.intersection(ray).boundary
                        
                        # TODO: Parfois la liste de points renvoyée est vide alors qu'elle ne devrait pas
                        if len(points_list):
                            # get the nearest point from bot
                            nearest_point = ShapesUtils.get_nearest_point(self._bot.shape.centroid, points_list)
                            obj_in_fov.append({
                                "distance": nearest_point.distance(self._bot.shape.centroid),
                                "name": item.friendly_name,
                                "object_type": item.object_type,
                                "angle": relative_angle,
                                "obj_id": item.id,
                                "origin": self.bot.shape.centroid.coords.xy,
                                "origin_ry": self.bot.ry,
                            })
            relative_angle += self._precision

        # keep only objects in the foreground
        visible_objects = self._keep_nearest_elements(obj_in_fov)

        return self._create_detected_objects(visible_objects)

    def __str__(self) -> str:
        return f"{self.name} (fov: {self.fov}, interval: {self.interval}, distance: {self.distance})"
