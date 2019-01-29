import random

from PIL import Image

from boop import colours, drawing, output, BoopError, logger


def make_random_ball_image(
    image_size, number_of_dots, centre_range, fade_range, colour_generator, mode
):

    image = Image.new(mode, image_size)
    for _ in range(0, number_of_dots):
        centre, inner_radius, fade_distance, colour = random_ball(
            image.size, centre_range, fade_range, colour_generator
        )
        image = drawing.add_ball(
            image, centre, inner_radius, fade_distance, False, colour
        )

    return image


def random_ball(image_size, centre_range, fade_range, colour_generator):

    height, width = image_size
    centre = (random.randint(0, height), random.randint(0, width))

    minimum_centre_radius, maximum_centre_radius = centre_range
    inner_radius = random.randint(minimum_centre_radius, maximum_centre_radius)

    minimum_fade_distance, maximum_fade_distance = fade_range
    fade_distance = random.randint(minimum_fade_distance, maximum_fade_distance)

    return centre, inner_radius, fade_distance, colour_generator()


def reduce_palette(image, palette_size):
    return apply_pallete(image, palette_size, image)


def apply_pallete(palette_image, palette_size, image):
    converted_palette_image = palette_image.quantize(colors=palette_size)
    return image.quantize(palette=converted_palette_image)


def generate_shrinked_balls(ball_list):
    """
    Given a list of balls makes all of them smaller, if a ball ceases to exist in the process
    doesnt yield it
    """
    for location, centre, fade, colour in ball_list:
        centre, fade = shrink_ball(centre, fade)
        if centre + fade > 0:
            yield(location, centre, fade, colour)


def shrink_ball(centre, fade):
    """
    takes a balls information and makes it smaller
    """
    if centre:
        centre = centre - 1

    if fade:
        fade = fade - 1

    return centre, fade


def fading_balls_video():

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

        for location, centre, fade, colour in ball_details:
            drawing.add_ball(image, location, centre, fade, False, colour)

        output.save(image, display=False)
        ball_details = [ball for ball in generate_shrinked_balls(ball_details)]


def changing_colour_balls_video():

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

        for location, centre, fade, colour in ball_details:
            drawing.add_ball(image, location, centre, fade, False, colour)

        output.save(image, display=False)
        ball_details = [ball for ball in generate_shrinked_balls(ball_details)]


if __name__ == "__main__":
    fading_balls_image()
