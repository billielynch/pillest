import random

from . import maths


MIN_COLOUR = 0
MAX_COLOUR = 255
COLOUR_CODOMAIN=(MIN_COLOUR, MAX_COLOUR)


def scale_colour(value, max_value):
    return int(value/max_value*MAX_COLOUR)


def random_saturation():
    return random.randint(MIN_COLOUR, MAX_COLOUR)


def random_rgb():
    return (
        random_saturation(),
        random_saturation(),
        random_saturation()
    )


def adjust_saturation(ratio: int, colour=None):
    try:
        return tuple(int(ratio * value) for value in colour)
    except TypeError:
        return int(ratio * colour)


def add_colours(c1, c2):
    try:
        assert len(c1) == len(c2)
    except TypeError:
        return maths.restrict_value(COLOUR_CODOMAIN, c1 + c2)
    else:
        colour_sum = (s1 + s2 for s1, s2 in zip(c1, c2))
        return tuple(maths.restrict_value(COLOUR_CODOMAIN, value) for value in colour_sum)



