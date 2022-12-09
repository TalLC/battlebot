from business.shapes import Shapes
from utils.geometry import Point2D

SQUARE = []
TRIANGLE = []


class ShapeFactory:
    @staticmethod
    def create_shape(name, o, radius=None, resolution=None, width=None):
        if name == 'square':
            return Shapes.Square(Point2D(o[0], o[1]), width)
        elif name == 'circle':
            return Shapes.Circle(Point2D(o[0], o[1]), radius, resolution)
        else:
            return None
