import mock

from boop import maths


@mock.patch('numpy.clip', autospec=True)
def test_clip_with_min_and_max_calls_numpy(mocked_method):
    maths.clip(1, min=2, max=3)
    mocked_method.assert_called_once_with(a=1, a_max=3, a_min=2)


@mock.patch('numpy.clip', autospec=True)
def test_clip_with_min_calls_numpy(mocked_method):
    maths.clip(1, min=2)
    mocked_method.assert_called_once_with(a=1, a_max=None, a_min=2)


@mock.patch('numpy.clip', autospec=True)
def test_clip_with_max_calls_numpy(mocked_method):
    maths.clip(1, max=3)
    mocked_method.assert_called_once_with(a=1, a_max=3, a_min=None)
