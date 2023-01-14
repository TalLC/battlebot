from math import radians, cos, sin


def get_nearest_point(point, list_points: list):
    # Find the distances between each point and point A
    distances = [point.distance(p) for p in list_points]
    # Find the index of the point with the minimum distance
    min_index = distances.index(min(distances))

    return list_points[min_index]


def calculate_point_coords(origin: tuple, distance: float, angle: float) -> tuple:
    coords = (origin[0] + distance * cos(radians(angle)),
              origin[1] + distance * sin(radians(angle)))

    return coords


def get_radius(element):
    return element.exterior.distance(element.centroid)
