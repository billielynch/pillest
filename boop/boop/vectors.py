import math


def vector_magnitude(v1, v2):

    x1, y1 = v1
    x2, y2 = v2
    component_form = ((x1 - x2), (y1 - y2))
    return magnitude(component_form)


def magnitude(vector):
    x, y = vector
    return math.sqrt(x * x + y * y)


def halve(vector):
    width, height = vector
    centre_height = int(height / 2)
    centre_width = int(width / 2)
    return (centre_width, centre_height)
