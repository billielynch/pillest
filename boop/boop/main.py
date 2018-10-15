import random

import numpy
from PIL import Image

from boop import colours, images, maths, output


def add_ball(image, centre, inner_radius, fade_distance, inverted, colour):
    outer_radius = fade_distance + inner_radius
    x_max, y_max = image.size

    top_left_corner = numpy.subtract(centre, outer_radius)
    corrected_top_left_corner = maths.clip(top_left_corner, min=0)

    bottom_right_corner = numpy.add(centre, outer_radius)
    corrected_bottom_right_corner = maths.clip(bottom_right_corner, max=[x_max, y_max])

    for y in range(
        corrected_top_left_corner.item(1), corrected_bottom_right_corner.item(1)
    ):
        for x in range(
            corrected_top_left_corner.item(0), corrected_bottom_right_corner.item(0)
        ):
            pixel_loc = (x, y)

            vector = numpy.subtract(pixel_loc, centre)
            distance_from_centre = int(numpy.linalg.norm(vector))

            restricted_distance = maths.clip(
                distance_from_centre, min=inner_radius, max=outer_radius
            )

            fade_progress = restricted_distance - inner_radius

            ratio = fade_progress / fade_distance
            ratio = 1 - ratio if not inverted else ratio
            adjusted_colour = colours.adjust_saturation(ratio, colour)
            current_colour = images.get_pixel(image, pixel_loc)
            colour_value = colours.add_colours(adjusted_colour, current_colour)
            image = images.put_pixel(image, pixel_loc, colour_value)

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


def draw_balls(image, ball_details):

    updated_balls = list()

    for location, centre, fade, colour in ball_details:
        add_ball(image, location, centre, fade, False, colour)

        if centre:
            centre = centre - 1

        if fade:
            fade = fade - 1

        if centre + fade > 0:
            updated_balls.append((location, centre, fade, colour))

    return updated_balls


def fading_balls_image():

    size = (100, 100)
    ball_details = []
    centre_range = (0, 10)
    fade_range = (10, 20)

    for _ in range(0, 100):

        image = Image.new("RGB", size)
        new_ball = random.choice([True, True, False])

        if new_ball:
            details = random_ball(
                size, centre_range, fade_range, colour_generator=colours.random_rgb
            )
            ball_details.append(details)

        ball_details = draw_balls(image, ball_details)
        output.save(image, display=False)


if __name__ == "__main__":
    fading_balls_image()
