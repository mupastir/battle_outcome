from abc import ABC, abstractmethod
from typing import Iterable, List

from units import BaseUnit
from utils import UnitsNumber, geometric_mean


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

    def validate_units(self, units):
        if not self.MIN_UNITS_NUMBER <= len(units) <= self.MAX_UNITS_NUMBER:
            raise UnitsNumber

    @abstractmethod
    def attack_probability(self):
        pass

    @abstractmethod
    def damage(self, enemy_squad):
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
        return geometric_mean([unit.attack_success for unit in self.units])

    def damage(self, enemy_squad: BaseSquad):
        damage_inflicted = sum([unit.damage for unit
                                in self.units])
        enemy_squad.damaged(damage_inflicted)
        for unit in self.units:
            unit.up_experience()

    def damaged(self, damage_received):
        damage_per_unit = damage_received / len(self.units)
        for unit in self.units:
            unit.damaged(damage_per_unit)

    @property
    def is_active(self):
        return any(unit.is_alive() for unit in self.units)
