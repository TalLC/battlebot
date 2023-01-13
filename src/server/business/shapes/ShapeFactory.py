from enum import Enum
from shapely.geometry import Point, Polygon, LineString


class Shape(Enum):
    SQUARE = 'square'
    CIRCLE = 'circle'
    LINE = 'line'
    POINT = 'point'


class ShapeFactory:
    def __init__(self):
        self.shape_map = {
            Shape.SQUARE: self.create_square,
            Shape.CIRCLE: self.create_circle,
            Shape.LINE: self.create_line,
            Shape.POINT: self.create_point
        }

    def create_shape(self, shape, **kwargs):
        """
        This method create shape from enum `Shape`.
        Each shape needs dict of parameters :
            - square : o=tuples(x, y), width=int
            - circle : o=tuples(x, y)
            - line : coords=list(tuples(x,y))
            - point : o=tuples(x, y)
        """
        if shape not in self.shape_map:
            raise ValueError(f'Unsupported shape: {shape}')

        return self.shape_map[shape](**kwargs)

    @staticmethod
    def create_square(**kwargs):
        if 'o' not in kwargs and 'width' not in kwargs:
            raise ValueError('Origin and/or width are missing.')

        o = Point(kwargs['o'])
        width = kwargs['width']

        return Polygon([
            (o.x - width/2, o.y - width/2), (o.x + width/2, o.y - width/2),
            (o.x + width/2, o.y + width), (o.x, o.y + width)])

    @staticmethod
    def create_circle(**kwargs):
        if 'o' not in kwargs and 'radius' not in kwargs and 'resolution' not in kwargs:
            raise ValueError('Origin, radius and/or resolution are missing.')

        o = Point(kwargs['o'])
        radius = kwargs['radius']
        resolution = kwargs['resolution']

        return Point(o.x, o.y).buffer(distance=radius, resolution=resolution)

    @staticmethod
    def create_line(**kwargs):
        if 'coords' not in kwargs:
            raise ValueError('Coords are missing.')

        coordinates = kwargs['coords']

        return LineString(coordinates)

    @staticmethod
    def create_point(**kwargs):
        if 'coords' not in kwargs:
            raise ValueError('Coords are missing.')

        o = kwargs['o']

        return Point(o)
