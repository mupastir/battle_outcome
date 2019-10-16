import typing

from units import Soldier, Vehicle


class Squad:

    def __init__(self, *units: typing.Iterable[Soldier, Vehicle]):
        self.units = units

    def attack_probability(self):
        pass

    def damage(self):
        pass

    def is_active(self):
        return any(unit.is_active() for unit in self.units)
