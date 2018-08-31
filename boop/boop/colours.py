import logging
import random

from boop import BoopError, maths


MIN_COLOUR = 0
MAX_COLOUR = 255


class ColourError(BoopError):
    pass


def random_saturation():
    return random.randint(MIN_COLOUR, MAX_COLOUR)


def random_rgb():
    return (
        random_saturation(),
        random_saturation(),
        random_saturation()
    )


def random_palette(number_colours, mode=None, colour_generator=None):

    if mode and colour_generator:
        logging.warning("mode will be ignored")

    if not colour_generator:
        if mode in ['RGB', None]:
            colour_generator = random_rgb
        elif mode == 'L':
            colour_generator = random_saturation

    return [colour_generator() for _ in range(0, number_colours)]


def adjust_saturation(ratio: int, colour=None):
    try:
        return tuple(int(ratio * value) for value in colour)
    except TypeError:
        return int(ratio * colour)


def add_colours(c1, c2):
    try:
        assert len(c1) == len(c2)
    except TypeError:
        return maths.clip(c1 + c2, max=MAX_COLOUR, min=MIN_COLOUR)
    else:
        colour_sum = (s1 + s2 for s1, s2 in zip(c1, c2))
        return tuple(maths.clip(value, max=MAX_COLOUR, min=MIN_COLOUR) for value in colour_sum)
