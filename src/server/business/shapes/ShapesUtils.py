

def get_nearest_point(point, list_points: list):
    # Find the distances between each point and point A
    distances = [point.distance(p) for p in list_points]
    # Find the index of the point with the minimum distance
    min_index = distances.index(min(distances))

    return list_points[min_index]