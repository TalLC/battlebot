from math import sqrt
from shapely.geometry import Point, Polygon
from utils.geometry import Point2D


class Shape:
    @property
    def poly(self) -> Polygon:
        return self._poly

    def __init__(self, poly: Polygon = Point(0, 0)):
        self._poly = poly


class Square(Shape):

    @property
    def radius(self):
        return self._width

    def __init__(self, origin: Point2D, width):
        self._width = width
        super().__init__(Polygon([(origin.x - self._width/2, origin.y - self._width/2),
                                  (origin.x + self._width/2, origin.y - self._width/2),
                                  (origin.x + self._width/2, origin.y + self._width),
                                  (origin.x, origin.y + self._width)
                                  ]))


class Circle(Shape):

    @property
    def radius(self):
        return self._radius

    @property
    def resolution(self):
        return self._resolution

    def __init__(self, origin: Point2D, radius, resolution: int = 6):
        self._radius = radius
        self._resolution = resolution
        super().__init__(Point(origin.x, origin.y).buffer(distance=self._radius, resolution=self._resolution))
