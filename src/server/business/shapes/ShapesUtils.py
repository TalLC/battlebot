from __future__ import annotations

import math
from math import radians, cos, sin
from typing import TYPE_CHECKING
from business.shapes.ShapeFactory import ShapeFactory, Shape

if TYPE_CHECKING:
    from business.gameobjects.OrientedGameObject import OrientedGameObject


class ShapesUtils:

    @staticmethod
    def get_2d_distance_between(point1: tuple, point2: tuple) -> float:
        """
        Return the distance between two points
        """
        return math.dist(point1, point2)

    @staticmethod
    def get_nearest_point(point, list_points: list):
        # Find the distances between each point and point A
        distances = [point.distance(p) for p in list_points]
        # Find the index of the point with the minimum distance
        min_index = distances.index(min(distances))

        return list_points[min_index]

    @staticmethod
    def get_coordinates_at_distance(origin: tuple, distance: float, angle: float, is_degrees: bool = False) -> tuple:
        """
        Calculate new coordinates based on the distance and the angle.
        """
        # Convert angle from degrees to radians if needed
        angle = radians(angle) if is_degrees else angle
        return (
            origin[0] + (distance * cos(angle)),
            origin[1] + (distance * sin(angle))
        )

    @staticmethod
    def get_radius(element) -> float:
        """
        Get the radius value of a shape.
        """
        return element.exterior.distance(element.centroid)

    @staticmethod
    def cast_ray_on_objects(start_coordinates: tuple, end_coordinates: tuple, objects: list[OrientedGameObject]):
        """
        Cast a ray and return the objects that are in the way.
        """
        result = list()
        ray = ShapeFactory().create_shape(shape=Shape.LINE, coords=[start_coordinates, end_coordinates])

        # Check each object in the list
        for obj in objects:
            # Check if ray touches object's shape
            if obj.shape.intersects(ray):
                result.append(obj)

        return result
