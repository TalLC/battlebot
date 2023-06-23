from __future__ import annotations

import logging
import math
from abc import ABC
from itertools import groupby
from threading import Thread, Event
from time import sleep
from typing import TYPE_CHECKING, List

from business.gameobjects.GameObject import GameObject
from common.config import CONFIG_GAME
from business.gameobjects.entity.bots.equipments.scanner.interfaces.IScanner import IScanner
from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from business.shapes.ShapesUtils import ShapesUtils
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.mqtt.BotScannerDetectionMessage import BotScannerDetectionMessage
from consumer.webservices.messages.websocket.DebugBotDetectedObjects import DebugBotDetectedObjects

from common.PerformanceCounter import PerformanceCounter

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


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

    @PerformanceCounter.count
    def _get_fov_angles(self) -> (float, float):
        """
        Return absolutes max and min angles for scanning in degrees.
        """
        min_angle = (self._bot.ry_deg - self._fov / 2) % 360
        max_angle = (self._bot.ry_deg + self._fov / 2) % 360

        logging.debug(f"[{self._bot.name}] scanning from {min_angle} to {max_angle} [{self._distance}]")

        return min_angle, max_angle

    @staticmethod
    @PerformanceCounter.count
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
    @PerformanceCounter.count
    def _create_detected_objects(elements: List[dict]) -> List[DetectedObject]:
        """
        Return list of DetectedObject from raycasting's result.
        """
        def by_object_id(element: dict) -> str:
            return element['obj_id']

        list_detected_obj = list()
        r_raycast = sorted(elements, key=by_object_id)

        for obj_id, hits_group in groupby(r_raycast, by_object_id):
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

    @PerformanceCounter.count
    def _iterate_fov_angle(self, min_angle: float, max_angle: float) -> List[float]:
        """
        Return list of angles in fov.
        """
        angles = list()
        tmp_angle = min_angle
        for i in range(0, int(self._fov/self._precision)):
            if min_angle > max_angle and tmp_angle >= 360:
                tmp_angle = 0.0
            angles.append(tmp_angle)
            tmp_angle += self._precision
        return angles

    @PerformanceCounter.count
    def scanning(self) -> List[DetectedObject]:
        """
            Supra magic power +++ infinite mega raycasting the revenge of the return !
        """
        # Gathering all relevant map objects
        detected_objects = self._bot.bot_manager.game_manager.get_map_objects(
            bots=True,                      # Get all the bots
            tiles=True,                     # Get all the tiles
            non_walkable_only=True,         # Restrict Tiles to the ones we cannot walk on
            tile_objects=True,              # Get all the tiles objects
            collision_only=True,            # Restrict Tile objects to the ones with collisions only
            radius=self._distance,
            origin=self._bot.coordinates
        )

        # Removing our bot from the detected objects
        detected_objects = [o for o in detected_objects if o != self.bot]

        # Removing objects outside fov
        detected_objects = list(filter(self._filter_object_in_fov, detected_objects))

        # Calculate the angles of the field of view
        min_fov, max_fov = self._get_fov_angles()
        # Init relative angle from bot
        relative_angle = -1 * (self._fov / 2)

        # Get objects in FOV
        obj_in_fov = self._get_objects_from_fov(relative_angle, min_fov, max_fov, detected_objects)

        # keep only objects in the foreground
        visible_objects = self._keep_nearest_elements(obj_in_fov)

        return self._create_detected_objects(visible_objects)

    @PerformanceCounter.count
    def _filter_object_in_fov(self, game_object: GameObject) -> bool:
        """
        Remove objects outside the fov.
        """
        # Vecteur entre le joueur et l'objet
        vecteur_x = game_object.x - self.bot.x
        vecteur_z = game_object.z - self.bot.z

        # Angle entre le vecteur joueur-objet et le vecteur de direction du joueur
        angle_degrees = math.degrees(ShapesUtils.angle_between((vecteur_z, vecteur_x), self.bot.forward_vector))

        # Vérification si l'objet est dans le cône de vision
        if -1 * self.fov/2 <= angle_degrees <= self.fov/2:
            return True
        return False

    @PerformanceCounter.count
    def _get_objects_from_fov(self, relative_angle: float, min_fov: float, max_fov: float,
                              detected_objects: list) -> List[dict]:
        obj_in_fov = list()

        # Shoot ray every [precision value] degree
        for a in self._iterate_fov_angle(min_fov, max_fov):
            ray = ShapesUtils.create_ray_to_angle(self.bot.coordinates, a, self.distance)
            # Check if collision between ray and elements on the map.
            for item in detected_objects:
                object_in_ray = self._check_raycasting(relative_angle, item, ray)
                obj_in_fov.append(object_in_ray) if object_in_ray != dict() else None

            relative_angle += self._precision
        return obj_in_fov

    @PerformanceCounter.count
    def _check_raycasting(self, relative_angle, item, ray) -> dict:
        if item.shape.intersection(ray):
            # get all intersections points
            points_list = item.shape.intersection(ray).boundary

            # TODO: Parfois la liste de points renvoyée est vide alors qu'elle ne devrait pas
            if len(points_list):
                # get the nearest point from bot
                nearest_point = ShapesUtils.get_nearest_point(self._bot.shape.centroid, points_list)
                return {
                    "distance": nearest_point.distance(self._bot.shape.centroid),
                    "name": item.friendly_name,
                    "object_type": item.object_type,
                    "angle": relative_angle,
                    "obj_id": item.id,
                    "origin": self.bot.shape.centroid.coords.xy,
                    "origin_ry": self.bot.ry,
                }
        return dict()

    def __str__(self) -> str:
        return f"{self.name} (fov: {self.fov}, interval: {self.interval}, distance: {self.distance})"
