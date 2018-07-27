from typing import Tuple


def value_or_more(value: int, number: int) -> int:
    if number >= value:
        return number
    return value


def value_or_less(value: int, number: int) -> int:
    if number <= value:
        return number
    return value


def restrict_value(codomain: Tuple[int, int], number: int):
    floor, ceiling = codomain
    result = value_or_more(floor, number)
    return value_or_less(ceiling, result)
