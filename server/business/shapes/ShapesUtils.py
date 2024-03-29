from __future__ import annotations

import math
import numpy as np
from math import radians, cos, sin
from typing import TYPE_CHECKING, List
from shapely.geometry import LineString

from business.shapes.ShapeFactory import ShapeFactory, Shape
from common.PerformanceCounter import PerformanceCounter

if TYPE_CHECKING:
    from business.gameobjects.GameObject import GameObject


class ShapesUtils:

    @staticmethod
    def get_2d_distance_between(point1: tuple, point2: tuple) -> float:
        """
        Return the distance between two points
        """
        return math.dist(point1, point2)

    @staticmethod
    @PerformanceCounter.count
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
    def create_ray_to_angle(start_coordinates: tuple, angle: float, distance: float) -> LineString:
        """
        Return linestring that represents a ray starting from coordinates at an angle "angle"
        """
        # Calculate the end point of the ray
        end_coordinates = ShapesUtils.get_coordinates_at_distance(
            start_coordinates, distance, angle, is_degrees=True
        )

        # Create ray
        return ShapeFactory().create_shape(shape=Shape.LINE, coords=[start_coordinates, end_coordinates])

    @staticmethod
    def cast_ray_on_objects(start_coordinates: tuple, end_coordinates: tuple,
                            objects: List[GameObject]) -> List[GameObject]:
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

    @staticmethod
    def scalar(v1: tuple, v2: tuple) -> float:
        """
        Scalar product of two vectors.
        """
        return v1[0] * v2[0] + v1[1] * v2[1]

    @staticmethod
    def unit_vector(vector):
        """
        Returns the unit vector of the vector (normalization).
        """
        return vector / np.linalg.norm(vector)

    @staticmethod
    def angle_between(v1, v2):
        """
        Returns the angle in radians between vectors 'v1' and 'v2'
        """
        v1_u = ShapesUtils.unit_vector(v1)
        v2_u = ShapesUtils.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
