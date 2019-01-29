from boop import BoopError


class ShapeError(BoopError):
    pass


class Circle(object):

    def __init__(self, radius, colour, location, fade_radius=0):

        self.radius = radius
        self.colour = colour
        self.location = location



    def __str__(self):
        formatted_string = "\n".join(
            [
                'Circle',
                f'radius : {self.radius}',
                f'fade_radius : {self.fade_radius}',
                f'location : {self.location}',
                f'colour : {self.colour}'
            ]
        )

        return formatted_string

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        try:
            integer_value = int(value)
            assert value > 0
        except (TypeError, AssertionError):
            raise ShapeError('Invalid radius')
        self.__radius = integer_value


class FaderCircle(Circle):

    def __init__(self, fade_radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_radius = fade_radius

    @property
    def fade_radius(self):
        return self.__fade_radius

    @fade_radius.setter
    def fade_radius(self, value):
        try:
            integer_value = int(value)
            assert value >= 0
        except (TypeError, AssertionError):
            raise ShapeError('Invalid fade radius')
        self.__fade_radius = integer_value

    def fade(self):
        if self.fade_radius > 0:
            self.fade_radius = self.fade_radius - 1
        if self.radius > 1:
            self.radius = self.radius - 1







