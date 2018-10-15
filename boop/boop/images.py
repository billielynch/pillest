from typing import Tuple

from PIL import Image


class ImageError(Exception):
    pass


def get_pixel(image: Image, location: Tuple[int, int]):
    try:
        return image.getpixel(location)
    except IndexError as e:
        raise ImageError(f"{e}, location {location}")


def put_pixel(image: Image, location: Tuple[int, int], colour):
    try:
        image.putpixel(location, colour)
        return image
    except IndexError as e:
        raise ImageError(f"{e}, location {location} colour {colour}")
