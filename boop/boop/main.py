import logging
import random
from datetime import datetime

import click
import numpy
from PIL import Image

from boop import colours, images, maths, output


def add_ball(
    image, ball_centre_location, solid_colour_radius, fade_distance, inverted, colour
):
    ball_radius = fade_distance + solid_colour_radius
    x_max_pixel, y_max_pixels = image.size

    # finding the parts of the ball that are actually in the image
    top_left_corner = numpy.subtract(ball_centre_location, ball_radius)
    clipped_top_left_corner = maths.clip(top_left_corner, min=0)
    ball_min_x = clipped_top_left_corner.item(0)
    ball_min_y = clipped_top_left_corner.item(1)

    bottom_right_corner = numpy.add(ball_centre_location, ball_radius)
    clipped_bottom_right_corner = maths.clip(
        bottom_right_corner, max=[x_max_pixel, y_max_pixels]
    )
    ball_max_x = clipped_bottom_right_corner.item(0)
    ball_max_y = clipped_bottom_right_corner.item(1)

    for y in range(ball_min_y, ball_max_y):
        for x in range(ball_min_x, ball_max_x):
            pixel = (x, y)

            distance_from_centre = maths.distance_between_points_ints_only(
                x1=x, y1=y, x2=ball_centre_location[0], y2=ball_centre_location[1]
            )

            if distance_from_centre > ball_radius:
                continue

            if distance_from_centre < solid_colour_radius:
                absolute_fade_progress = 0
            else:
                absolute_fade_progress = distance_from_centre - solid_colour_radius

            if fade_distance < 0:
                raise ValueError(
                    "we cannot use negative numbers"
                    f" for fade distance (`{fade_distance}`)"
                )

            fade_percentage = (
                absolute_fade_progress / fade_distance if fade_distance > 0 else 0
            )
            fade_percentage = 1 - fade_percentage if not inverted else fade_percentage
            adjusted_colour = colours.adjust_saturation(
                ratio=fade_percentage, colour=colour
            )
            current_colour = images.get_pixel(image, pixel)
            colour_value = colours.add_colours(adjusted_colour, current_colour)
            image = images.put_pixel(image, pixel, colour_value)

    return image


def make_random_ball_image(
    image_size, number_of_dots, centre_range, fade_range, palette, mode
):

    image = Image.new(mode, image_size)
    for colour in random.choices(palette, k=number_of_dots):
        centre, inner_radius, fade_distance = random_ball(
            image.size, centre_range, fade_range
        )
        image = add_ball(image, centre, inner_radius, fade_distance, False, colour)

    return image


def random_ball(size, centre_range, fade_range, colour_generator=None):

    height, width = size
    minimum_centre_radius, maximum_centre_radius = centre_range
    minimum_fade_distance, maximum_fade_distance = fade_range

    centre = (random.randint(0, height), random.randint(0, width))
    inner_radius = random.randint(minimum_centre_radius, maximum_centre_radius)
    fade_distance = random.randint(minimum_fade_distance, maximum_fade_distance)

    if colour_generator:
        return centre, inner_radius, fade_distance, colour_generator()
    else:
        return centre, inner_radius, fade_distance


def reduce_palette(image, palette_size):
    return apply_pallete(image, palette_size, image)


def apply_pallete(palette_image, palette, image):
    converted_palette_image = palette_image.quantize(colors=palette)
    return image.quantize(palette=converted_palette_image)


def greyscale_balls(**kwargs):
    return make_random_ball_image(mode="L", **kwargs)


def randomcolour_balls(**kwargs):
    return make_random_ball_image(mode="RGB", **kwargs)


def white_balls(**kwargs):
    palette = [colours.MAX_COLOUR]
    return greyscale_balls(palette=palette, **kwargs)


def draw_balls_into_image(image, ball_details):
    for location, centre, fade_distance, colour in ball_details:
        add_ball(image, location, centre, fade_distance, False, colour)


def shrink_balls(ball_details):
    updated_balls = list()
    for location, centre, fade_distance, colour in ball_details:
        if centre + fade_distance > 1:
            if centre > 0:
                centre = centre - 1
            if fade_distance > 0:
                fade_distance = fade_distance - 1
            updated_balls.append((location, centre, fade_distance, colour))
    return updated_balls


def shrink_balls_alt(ball_details):

    updated_balls = list()

    for location, centre, fade_distance, colour in ball_details:
        if centre + fade_distance > 1:

            # reduces the solid colour radius first, then the fade radius
            if centre > 0:
                centre = centre - 1

            elif fade_distance > 1:
                fade_distance = fade_distance - 1

            updated_balls.append((location, centre, fade_distance, colour))

    return updated_balls


def fading_balls_images(dirpath):

    logging.info("generating a coloured fading ball image set")

    frames = 500
    image_size = (500, 500)
    logging.debug(f"image size: {image_size}")
    solid_colour_radius_choice_range = (10, 50)
    fade_radius_choice_range = (30, 120)

    list_of_balls = []
    images = []

    for count in range(0, frames):
        logging.info(f"generating frame {count} of {frames}")
        image = Image.new("RGB", image_size)
        new_ball = random.choice([True, True, False, False, False])

        if new_ball:
            ball_details = random_ball(
                image_size,
                solid_colour_radius_choice_range,
                fade_radius_choice_range,
                colour_generator=colours.random_rgb,
            )
            list_of_balls.append(ball_details)

        draw_balls_into_image(image, list_of_balls)
        images.append(image)
        list_of_balls = shrink_balls(list_of_balls)

    logging.info("completed generation")
    return images


@click.command()
@click.option("-d", "--dirname", help="directory name for the image set.")
@click.option(
    "--debug",
    is_flag=True,
    show_default=True,
    default=False,
    help="Use to show debug logging",
)
def main(dirname, debug):

    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="%(asctime)s %(levelname)8s: %(message)s", level=log_level
    )

    logging.debug(f"passed `{dirname}` as dirname")
    if not dirname:
        now = datetime.now()
        dirname = now.strftime("%Y-%m-%d-%H%M")
        logging.debug(f"set `{dirname}` as dirname")

    dirpath = output.make_image_set_path(image_set_name=dirname)
    if not dirpath:
        logging.debug("bailing due to no dirpath")
        return 0
    
    images = fading_balls_images(dirpath)

    image_counter = 0
    for image in images:
        output.save(
            image,
            display=False,
            filename=f"image{image_counter:04d}",
            directory_path=dirpath,
        )
        image_counter += 1


if __name__ == "__main__":
    main()
