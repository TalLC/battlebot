from math import radians, cos, sin


class ShapesUtils:

    @staticmethod
    def get_nearest_point(point, list_points: list):
        # Find the distances between each point and point A
        distances = [point.distance(p) for p in list_points]
        # Find the index of the point with the minimum distance
        min_index = distances.index(min(distances))

        return list_points[min_index]

    @staticmethod
    def get_coordinates_at_distance(origin: tuple, distance: float, angle: float) -> tuple:
        """
        Calculate new coordinates based on the distance and the angle.
        """
        return (
            origin[0] + distance * cos(radians(angle)),
            origin[1] + distance * sin(radians(angle))
        )

    @staticmethod
    def get_radius(element) -> float:
        """
        Get the radius value of a shape.
        """
        return element.exterior.distance(element.centroid)