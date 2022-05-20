import logging
from os import environ

IMAGES_DIR = "BOOP_IMAGES_DIR"
DEBUG = "BOOP_DEBUG"

debug = environ.get(DEBUG, None)


class BoopError(Exception):
    pass


logger = logging.getLogger("boop")
logger.setLevel(logging.DEBUG if debug else logging.INFO)
