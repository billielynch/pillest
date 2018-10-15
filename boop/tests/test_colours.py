import mock
import pytest

from boop import colours


@mock.patch("random.randint", autospec=True)
def test_random_saturation_calls_random_with_expected_params(mocked_class):
    colours.random_saturation()
    mocked_class.assert_called_once_with(colours.MIN_COLOUR, colours.MAX_COLOUR)


@mock.patch("boop.colours.random_saturation", autospec=True)
def test_random_rgb_calls_random_saturation_three_times(mocked_class):
    colours.random_rgb()
    expected_calls = 3
    assert (
        mocked_class.call_count == expected_calls
    ), f"random_rgb was called {mocked_class.call_count} times, should have been {expected_calls}"


def test_adjust_saturation_where_colour_is_iterable_and_ratio_is_zero_expected_result():
    colour = (100, 120, 140)
    result = colours.adjust_saturation(0, colour)
    assert result == (0, 0, 0)


def test_adjust_saturation_where_colour_is_iterable_and_ratio_is_more_than_1_expected_result():
    colour = (100, 120, 140)
    result = colours.adjust_saturation(10, colour)
    assert result == (1000, 1200, 1400)


def test_adjust_saturation_where_colour_is_iterable_and_ratio_is_less_than_1_expected_result():
    colour = (100, 120, 140)
    result = colours.adjust_saturation(0.7, colour)
    assert result == (70, 84, 98)


def test_adjust_saturation_where_colour_is_iterable_and_ratio_is_1_expected_result():
    colour = (100, 120, 140)
    result = colours.adjust_saturation(1, colour)
    assert result == (100, 120, 140)


def test_adjust_saturation_where_colour_is_number_and_ratio_is_zero_expected_result():
    colour = 129
    result = colours.adjust_saturation(0, colour)
    assert result == 0


def test_adjust_saturation_where_colour_is_number_and_ratio_is_more_than_1_expected_result():
    colour = 129
    result = colours.adjust_saturation(10, colour)
    assert result == 1290


def test_adjust_saturation_where_colour_is_number_and_ratio_is_less_than_1_expected_result():
    colour = 129
    result = colours.adjust_saturation(0.7, colour)
    assert result == 90


def test_adjust_saturation_where_colour_is_number_and_ratio_is_1_expected_result():
    colour = 129
    result = colours.adjust_saturation(1, colour)
    assert result == 129


def test_adjust_saturation_where_ratio_is_less_than_1():
    with pytest.raises(colours.ColourError):
        colours.adjust_saturation(-3, 43)


def test_random_palette_default_generator_zero_colours_expected_result():
    with pytest.raises(colours.ColourError):
        colours.random_palette(0)


@mock.patch("boop.colours.random_rgb", autospec=True)
def test_random_palette_default_generator_with_one_colour_called_once(mocked_method):
    colours.random_palette(1)
    mocked_method.assert_called_once_with()


def test_random_palette_default_generator_with_one_colour_expected_result():
    assert len(colours.random_palette(1)) == 1


@mock.patch("boop.colours.random_rgb", autospec=True)
def test_random_palette_default_generator_many_colours_called_that_many_times(
    mocked_method
):
    colours.random_palette(100)
    expected_call = 100
    assert (
        mocked_method.call_count == expected_call
    ), f"random_saturation was called {mocked_method.call_count} times, should have been {expected_call}"


def test_random_palette_default_generator_with_many_colours_expected_result():
    assert len(colours.random_palette(11)) == 11


def test_random_palette_rgb_mode_zero_colours_expected_result():

    with pytest.raises(colours.ColourError):
        colours.random_palette(0)


@mock.patch("boop.colours.random_saturation", autospec=True)
def test_random_palette_l_mode_with_one_colour_called_once(mocked_method):
    colours.random_palette(1, mode="L")
    mocked_method.assert_called_once_with()


def test_random_palette_l_mode_with_one_colour_expected_result():
    assert len(colours.random_palette(1, mode="L")) == 1


@mock.patch("boop.colours.random_saturation", autospec=True)
def test_random_palette_l_mode_many_colours_called_that_many_times(mocked_method):
    colours.random_palette(100, mode="L")
    expected_call = 100
    assert (
        mocked_method.call_count == expected_call
    ), f"random_saturation was called {mocked_method.call_count} times, should have been {expected_call}"


def test_random_palette_l_mode_with_many_colours_expected_result():
    assert len(colours.random_palette(11, mode="L")) == 11


@mock.patch("boop.colours.random_rgb", autospec=True)
def test_random_palette_rgb_mode_with_one_colour_called_once(mocked_method):
    colours.random_palette(1, mode="RGB")
    mocked_method.assert_called_once_with()


def test_random_palette_rgb_mode_with_one_colour_expected_result():
    assert len(colours.random_palette(1, mode="RGB")) == 1


@mock.patch("boop.colours.random_rgb", autospec=True)
def test_random_palette_rgb_mode_many_colours_called_that_many_times(mocked_method):
    colours.random_palette(100, mode="RGB")
    expected_call = 100
    assert (
        mocked_method.call_count == expected_call
    ), f"random_saturation was called {mocked_method.call_count} times, should have been {expected_call}"


def test_random_palette_rgb_mode_with_many_colours_expected_result():
    assert len(colours.random_palette(11, mode="RGB")) == 11


def test_add_colours_array():
    result = colours.add_colours((122, 123, 124), (10, 13, 20))
    assert result == (132, 136, 144)


def test_add_colours_array_clipping():
    result = colours.add_colours((222, 233, 244), (210, 13, 20))
    assert result == (255, 246, 255)


def test_add_colours_number():
    result = colours.add_colours(240, 10)
    assert result == 250


def test_add_colours_number_clipping():
    result = colours.add_colours((222, 233, 244), (210, 13, 20))
    assert result == (255, 246, 255)
