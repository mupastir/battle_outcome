import typing
from abc import ABC, abstractmethod

from units import BaseUnit
from utils import geometric_avg


class BaseSquad(ABC):

    def __init__(self):
        super().__init__()

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

    def __init__(self, units: typing.Iterable[BaseUnit]):
        super().__init__()
        self.units = list(units)

    @property
    def attack_probability(self):
        return geometric_avg([unit.attack_success for unit in self.units])

    def damage(self, enemy_squad: BaseSquad):
        damage_inflicted = sum([unit.damage for unit
                                in self.units])
        enemy_squad.damaged(damage_inflicted)

    def damaged(self, damage_received):
        damage_per_unit = damage_received / len(self.units)
        for unit in self.units:
            unit.damaged(damage_per_unit)

    @property
    def is_active(self):
        return any(unit.is_alive() for unit in self.units)
