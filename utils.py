from functools import reduce

from _operator import mul


class MaxExperienceException(ValueError):
    pass


class MinHealthException(ValueError):
    pass


class MinSquadsException(ValueError):
    pass


class MinArmiesException(ValueError):
    pass


class UnitsNumberException(ValueError):
    pass


class StrategyValue(ValueError):
    pass


def geometric_mean(args):
    return reduce(mul, args) ** (1.0 / len(args))
