from datetime import datetime
from os import environ, path
from subprocess import call

from boop import IMAGES_DIR


class OutputError(Exception):
    pass


class PNGFormat(object):
    driver = 'PNG'
    extension = '.png'


def save(image, display=True):

    absfile_path = save_path(image_format=PNGFormat)
    image.save(absfile_path, PNGFormat.driver)

    if display:
        show(absfile_path)


def root_path():
    env_var_value = environ.get(IMAGES_DIR, None)

    if not env_var_value:
        raise OutputError(f"Please set the '{IMAGES_DIR}' environment variable")

    absolute_path = path.abspath(env_var_value)
    return absolute_path


def save_path(image_format, counter=None):

    if counter is None:
        counter = 0

    directory = root_path()

    iso_date = datetime.today().isoformat()
    filename = iso_date + '_' + str(counter) + image_format.extension
    filepath = path.join(directory, filename)

    if path.exists(filepath):
        return save_path(image_format=image_format, counter=counter)
    else:
        return filepath


def show(filepath):
    call(["eog", filepath])
