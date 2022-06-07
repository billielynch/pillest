import random
from typing import Tuple

import numpy

from boop import BoopError, logger, maths

MIN_COLOUR = 0
MAX_COLOUR = 255


class ColourError(BoopError):
    pass


def random_saturation() -> int:
    """
        Returns an even distribution of (0,255) which
        is intended to be used to generate the RGB

    Returns:
        int: a random number (0, 255)
    """
    return random.randint(MIN_COLOUR, MAX_COLOUR)


def random_rgb() -> Tuple[int, int, int]:
    """
        Returns a tuple that can be used as a single colour

    Returns:
        Tuple[int, int, int]: a thruple of ints of (0,255)
    """
    return (random_saturation(), random_saturation(), random_saturation())


def random_palette(number_of_colours: int, mode="RGB"):
    """
        Creates a list of colours in the prefered mode

    Args:
        number_of_colours (int): how many colours you want
        mode (_type_, optional): _description_. Defaults to RGB, can also do black/white if given 'L'.

    Returns:
        _type_:
    """

    if number_of_colours < 1:
        logger.error("you probably shouldnt call this if you want 0 colours")

    if number_of_colours == 1:
        logger.warning(
            "try using a colour generator method if you want a single colour"
        )

    if mode == "L":
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
