import random

from PIL import Image

from . import vectors, images, colours, maths


def add_ball(image, centre, inner_radius, fade_distance, inverted, colour):
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


def make_ball_image(image_size, number_of_dots, centre_range, fade_range, palette, mode):

    size = (image_size, image_size)
    minimum_centre_radius, maximum_centre_radius = centre_range
    minimum_fade_distance, maximum_fade_distance = fade_range

    image = Image.new(mode, size)

    for colour in random.choices(palette, k=number_of_dots):
        inner_radius = random.randint(minimum_centre_radius, maximum_centre_radius)
        fade_distance = random.randint(minimum_fade_distance, maximum_fade_distance)
        centre = (random.randint(0, image_size), random.randint(0, image_size))

        image = add_ball(image, centre, inner_radius, fade_distance, False, colour)

    return image


def reduce_palette(image, palette_size):
    return apply_pallete(image, palette_size, image)


def apply_pallete(palette_image, colours, image):
    converted_palette_image = palette_image.quantize(colors=colours)
    return image.quantize(palette=converted_palette_image)


def greyscale_balls(image_size, number_of_dots, centre_range, fade_range, palette):
    mode = 'L'
    return make_ball_image(image_size, number_of_dots, centre_range, fade_range, palette, mode)


def colour_balls(image_size, number_of_dots, centre_range, fade_range, palette):
    mode = 'RGB'
    return make_ball_image(image_size, number_of_dots, centre_range, fade_range, palette, mode)


def white_balls(image_size, number_of_dots, centre_range, fade_range):
    palette = [colours.MAX_COLOUR]
    return greyscale_balls(image_size, number_of_dots, centre_range, fade_range, palette)


def random_colour_balls(image_size, number_of_dots, centre_range, fade_range, num_colours=200):
    palette = [colours.random_rgb() for _ in range(0, num_colours)]
    return greyscale_balls(image_size, number_of_dots, centre_range, fade_range, palette)


def image_pallete_balls(image_size, number_of_dots, centre_range, fade_range, image_file):
    image = Image.open(image_file)
    palette = [colour for _, colour in image.getcolors(maxcolors=10000000)]
    colour_balls(image_size, number_of_dots, centre_range, fade_range, palette).show()


if __name__ == '__main__':

    image_pallete_balls(1000, 100, (0,10), (5,30), 'pillest/files/galaxy.jpg')