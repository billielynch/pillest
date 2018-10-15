import numpy


def clip(item, min=None, max=None):
    return numpy.clip(a=item, a_max=max, a_min=min)
