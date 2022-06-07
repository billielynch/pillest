import math

import numpy


def clip(item, min=None, max=None):
    return numpy.clip(a=item, a_max=max, a_min=min)


def distance_between_points_ints_only(x1: int, y1: int, x2: int, y2: int) -> int:
    x = abs(x2 - x1)
    y = abs(y2 - y1)
    z = math.sqrt(x * x + y * y)
    return math.ceil(z)
