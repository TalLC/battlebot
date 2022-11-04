from math import cos, sin, atan2, sqrt
from shapely.geometry import Polygon
import shapely.affinity


class Point2D:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({round(self.x, 3)}, {round(self.y, 3)})'


class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_angle(cls, angle):
        return cls(x=cos(angle), y=sin(angle))

    @classmethod
    def from_points(cls, a: Point2D, b: Point2D):
        return cls(x=b.x - a.x, y=b.y - a.y)

    def __str__(self):
        return f'({round(self.x, 3)}, {round(self.y, 3)})'

    def __sub__(self, other):
        """subtraction."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """addition."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __abs__(self):
        """Absolute value (magnitude) of the vector."""
        return sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        """The scalar (dot) product of self and other. Both must be vectors."""

        if not isinstance(other, Vector2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y

    def distance_to(self, other):
        """The distance between vectors self and other."""
        return abs(self - other)

    def angle_to(self, other):
        """ The angle between vectors self and other."""
        return atan2(other.y, other.x) - atan2(self.y, self.x)


if __name__ == '__main__':
    import logging
    import numpy as np
    logging.basicConfig(level=logging.INFO)
    # n = np.array()
    # bot = Point2D(0, 0)
    # bot_ry = 0.0
    # obj = Point2D(1, 1)
    #
    # v_bot = Vector2D.from_angle(bot_ry)
    # v_bot_obj = Vector2D.from_points(bot, obj)
    #
    # logging.info(f"{v_bot.angle_to(v_bot_obj) * 180/pi}")
    # logging.info(f"{v_bot_obj.angle_to(v_bot) * 180/pi}")
    # poly1 = Shape([(0, 0), (4, 2), (3, 1), (3, 7), (4, 1), (5, 0), (1, 3) ])
    # circle1 = Shape.circle(1, 3, (3, 3))
    # rect1 = Shape.rect(2, 1, (3, 3))
    # square1 = Shape.square(4, (0, 0))
    square1 = Polygon([(0, 0), (1, 0), (1, 1), (1, 1)])
    # triangle1 = Shape.triangle(1, (3, 3))
    square2 = shapely.affinity.translate(square1, 2-square1.centroid.x, 2-square1.centroid.y)
    # logging.info(f"poly : {poly1}")
    # logging.info(f"circle : {circle1}")
    # logging.info(f"rectangle : {rect1}")
    logging.info(f"square1 : {square1}")
    logging.info(f"square2 : {square2}")
    logging.info(f"square2 : {square2.centroid}")
    # logging.info(f"triangle :{triangle1}")

