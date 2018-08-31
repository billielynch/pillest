import random
from typing import Tuple

import numpy

from boop import BoopError, logger, maths


MIN_COLOUR = 0
MAX_COLOUR = 255


class ColourError(BoopError):
    pass


def random_saturation() -> int:
    return random.randint(MIN_COLOUR, MAX_COLOUR)


def random_rgb() -> Tuple[int, int, int]:
    return (
        random_saturation(),
        random_saturation(),
        random_saturation()
    )


def random_palette(number_of_colours: int, mode=None):

    if number_of_colours < 1:
        raise ColourError(f"Can only generate a positive number of colours not {number_of_colours}")

    if number_of_colours == 1:
        logger.warning('try using a colour generator method if you want a single colour')

    if mode == 'RGB':
        colour_generator = random_rgb
    elif mode == 'L':
        colour_generator = random_saturation
    else:
        colour_generator = random_rgb

    return [colour_generator() for _ in range(0, number_of_colours)]


def adjust_saturation(ratio: float, colour):

    if ratio < 0:
        raise ColourError("Ratio parameter should be a non-negative number")

    try:
        return tuple(int(ratio * value) for value in colour)
    except TypeError:
        return int(ratio * colour)


def add_colours(c1, c2):
    added_colours = numpy.add(c1, c2)
    result = maths.clip(added_colours, max=MAX_COLOUR, min=MIN_COLOUR)

    try:
        return tuple(result)
    except TypeError:
        return int(result)
