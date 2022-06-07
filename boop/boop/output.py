import logging
import os
from os import environ, path
from subprocess import call

from boop import IMAGES_DIR


class OutputError(Exception):
    pass


class PNGFormat(object):
    driver = "PNG"
    extension = ".png"


def save(image, filename, directory_path, display=True):
    """_summary_

    Args:
        image (_type_): the Image
        filename (_type_): string for filename
        image_set_name (_type_): string for the image set name
        display (bool, optional): whether to open the image on save. Defaults to True. #TODO: this should not be here
    """

    FORMAT = PNGFormat

    filepath = path.join(directory_path, filename + FORMAT.extension)
    image.save(filepath, FORMAT.driver)
    logging.debug(f"saved image to {filepath}")

    if display:
        show(filepath)


def get_root_path():
    env_var_value = environ.get(IMAGES_DIR, None)

    if not env_var_value:
        raise OutputError(
            f"Please set the '{IMAGES_DIR}' environment variable, current it is '{env_var_value}'"
        )

    absolute_path = path.abspath(env_var_value)
    logging.debug(f"found root path as: {absolute_path}")
    return absolute_path


def make_image_set_path(image_set_name):

    root_directory = get_root_path()
    directory_path = path.join(root_directory, image_set_name)

    if path.exists(directory_path):
        logging.warning(f"'{directory_path}' already exists, this might get messy")
        input_given = input("type nothing to bail:")
        if input_given == "":
            return None
    else:
        os.mkdir(directory_path)
        logging.info(f"created {directory_path}")

    return directory_path


def show(filepath):
    call(["eog", filepath])
