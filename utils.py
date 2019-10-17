from functools import reduce

from _operator import mul


class MaxExperienceException(Exception):
    pass


class UnitsNumber(Exception):
    pass


def geometric_avg(args):
    prod = reduce(mul, args, 0)
    return prod ** (1.0 / len(args))
