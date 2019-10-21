from abc import ABC, abstractmethod
from typing import Iterable, List

from models.units import BaseUnit
from utils import UnitsNumberException, geometric_mean


class BaseSquad(ABC):
    MIN_UNITS_NUMBER = 5
    MAX_UNITS_NUMBER = 10

    def __init__(self, units: Iterable[BaseUnit]):
        super().__init__()
        self.units = list(units)

    @property
    def units(self) -> List[BaseUnit]:
        return self._units

    @units.setter
    def units(self, value: List[BaseUnit]):
        self.validate_units(value)
        self._units = value

    def validate_units(self, units: List[BaseUnit]):
        if not self.MIN_UNITS_NUMBER <= len(units) <= self.MAX_UNITS_NUMBER:
            raise UnitsNumberException

    @abstractmethod
    def attack_probability(self):
        pass

    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def damaged(self, damage_received):
        pass

    @abstractmethod
    def is_active(self):
        pass


class Squad(BaseSquad):

    def __init__(self, units: Iterable[BaseUnit]):
        super().__init__(units)

    @property
    def attack_probability(self):
        if self.is_active:
            return geometric_mean([unit.attack_success for unit in self.units])
        return 0

    @property
    def damage(self):
        for unit in self.units:
            unit.up_experience()
        return sum([unit.damage for unit
                    in self.units])

    def damaged(self, damage_received):
        damage_per_unit = damage_received / len(self.units)
        for unit in self.units:
            unit.damaged(damage_per_unit)

    @property
    def is_active(self):
        return any(unit.is_alive() for unit in self.units)
