import numpy

from . import colours, images, maths


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
