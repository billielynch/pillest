import random

from PIL import Image

from . import vectors, images, colours, maths


def single_ball_image(size, centre=None, fade_distance=None, inner_radius=None, inverted=False):

    if not centre:
        centre = vectors.halve(size)

    if not inner_radius:
        inner_radius = 0

    if not fade_distance:
        fade_distance = vectors.magnitude(centre) - inner_radius

    mode = 'L'
    image = Image.new(mode, size)
    add_ball(image, centre, inner_radius, fade_distance, inverted)
    return image


def add_ball(image, centre, inner_radius, fade_distance, inverted):
    outer_radius = fade_distance + inner_radius
    x_max, y_max = image.size
    x_centre, y_centre = centre

    y_min = maths.value_or_more(0, y_centre - outer_radius)
    y_max = maths.value_or_less(y_max, y_centre + outer_radius)

    x_min = maths.value_or_more(0, x_centre - outer_radius)
    x_max = maths.value_or_less(x_max, x_centre + outer_radius)

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            pixel_loc = (x, y)

            distance_from_centre = vectors.vector_magnitude(pixel_loc, centre)
            restricted_distance = maths.restrict_value(codomain=(inner_radius, outer_radius), number=distance_from_centre)
            fade_progress = restricted_distance - inner_radius

            ratio = fade_progress/fade_distance
            ratio = 1 - ratio if not inverted else ratio
            depth = colours.adjust_saturation(ratio, colours.MAX_COLOUR)
            colour = maths.restrict_value(
                codomain=colours.COLOUR_CODOMAIN,
                number=images.get_pixel(image, pixel_loc) + depth
            )
            image = images.put_pixel(image, pixel_loc, colour)

    return image


def reduce_palette(image, palette_size):
    return apply_pallete(image, palette_size, image)


def apply_pallete(palette_image, colours, image):
    converted_palette_image = palette_image.quantize(colors=colours)
    return image.quantize(palette=converted_palette_image)


def make_ball_image(image_size, number_of_dots, centre_range, fade_range):
    mode = 'RGB'
    size = (image_size, image_size)

    minimum_centre_radius, maximum_centre_radius = centre_range
    minimum_fade_distance, maximum_fade_distance = fade_range

    image = Image.new(mode, size)

    for _ in range(0, number_of_dots):
        inner_radius = random.randint(minimum_centre_radius, maximum_centre_radius)
        fade_distance = random.randint(minimum_fade_distance, maximum_fade_distance)
        centre = (random.randint(0, image_size), random.randint(0, image_size))

        image = add_ball(image, centre, inner_radius, fade_distance, False)

    return image


def make_colour_ball_image(image_size, number_of_dots, centre_range, fade_range, palette=None):
    mode = 'RGB'
    size = (image_size, image_size)

    minimum_centre_radius, maximum_centre_radius = centre_range
    minimum_fade_distance, maximum_fade_distance = fade_range

    image = Image.new(mode, size)

    if palette:
        chosen_colours = random.choices(palette, k=number_of_dots)
    else:
        chosen_colours = [colours.random_rgb() for _ in range(0, number_of_dots)]

    for colour in chosen_colours:
        inner_radius = random.randint(minimum_centre_radius, maximum_centre_radius)
        fade_distance = random.randint(minimum_fade_distance, maximum_fade_distance)
        centre = (random.randint(0, image_size), random.randint(0, image_size))

        image = add_colour_ball(image, centre, inner_radius, fade_distance, False, colour)

    return image


def add_colour_ball(image, centre, inner_radius, fade_distance, inverted, colour):
    outer_radius = fade_distance + inner_radius
    x_max, y_max = image.size
    x_centre, y_centre = centre

    y_min = maths.value_or_more(0, y_centre - outer_radius)
    y_max = maths.value_or_less(y_max, y_centre + outer_radius)

    x_min = maths.value_or_more(0, x_centre - outer_radius)
    x_max = maths.value_or_less(x_max, x_centre + outer_radius)

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            pixel_loc = (x, y)

            distance_from_centre = vectors.vector_magnitude(pixel_loc, centre)
            restricted_distance = maths.restrict_value(codomain=(inner_radius, outer_radius), number=distance_from_centre)
            fade_progress = restricted_distance - inner_radius

            ratio = fade_progress/fade_distance
            ratio = 1 - ratio if not inverted else ratio
            adjusted_colour = colours.adjust_saturation(ratio, colour)
            current_colour = images.get_pixel(image, pixel_loc)
            colour_value = colours.add_colours(adjusted_colour, current_colour)
            image = images.put_pixel(image, pixel_loc, colour_value)

    return image


if __name__ == '__main__':

    image = Image.open('pillest/files/galaxy.jpg')
    palette = [colour for _, colour in image.getcolors(maxcolors=10000000)]

    make_colour_ball_image(800, 200, (0, 5), (1, 100), palette).show()