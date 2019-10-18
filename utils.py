from functools import reduce

from _operator import mul


class MaxExperienceException(Exception):
    pass


class UnitsNumber(Exception):
    pass


def geometric_mean(args):
    return reduce(mul, args) ** (1.0 / len(args))
