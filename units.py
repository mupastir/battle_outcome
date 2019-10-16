import random
from functools import reduce
from _operator import mul
from abc import ABC, abstractmethod
import typing


class BaseUnit(ABC):

    def __init__(self, recharge: int):
        super().__init__()
        self.recharge = self.get_recharge(recharge)
        self.health = 100
        self.experience = 0

    def get_recharge(self, recharge):
        if not isinstance(recharge, int):
            raise TypeError
        return recharge

    @abstractmethod
    def up_experience(self):
        pass

    @abstractmethod
    def attack_success(self) -> float:
        pass

    @abstractmethod
    def damage(self) -> float:
        pass

    @abstractmethod
    def damaged(self, damage):
        pass

    def is_alive(self) -> bool:
        if self.health <= 0:
            return False
        return True


class Soldier(BaseUnit):

    def __init__(self, recharge: int):
        super().__init__(recharge)

    def up_experience(self):
        self.experience += 1

    @property
    def attack_success(self):
        return 0.5 * (1 + self.health / 100) * random.randint(
            50 + self.experience, 100) / 100

    @property
    def damage(self):
        return 0.05 + self.experience / 100

    def damaged(self, damage):
        self.health -= damage


class Vehicle(BaseUnit):
    OPERATORS_COUNT = 3
    MIN_RECHARGE = 1000
    MAX_RECHARGE = 2000

    def __init__(self, recharge: int, *operators: typing.Iterable[Soldier]):
        super().__init__(recharge)
        self.operators = list(*operators)
        self.total_health = self.health + (sum(self._operators_health)
                                           / len(self._operators_health))

    def get_recharge(self, recharge):
        recharge = super().get_recharge(recharge)
        if not(self.MIN_RECHARGE <= recharge <= self.MAX_RECHARGE):
            raise ValueError
        return recharge

    def up_experience(self):
        for operator in self.operators:
            if operator.is_alive():
                operator.up_experience()

    @property
    def operators(self):
        return self._operators

    @operators.setter
    def operators(self, value):
        self._operators = value
        if len(value) != self.OPERATORS_COUNT:
            raise ValueError

    @property
    def _operators_health(self):
        return [x.health for x in self.operators]

    @staticmethod
    def _geometric_avg(*attack_success):
        prod = reduce(mul, *attack_success, 0)
        return prod ** (1.0 / len(attack_success))

    @property
    def attack_success(self):
        if self.is_alive():
            return 0.5 * (1 + self.health / 100) * self._geometric_avg(
                [x.attack_success for x in self.operators])
        return 0

    @property
    def damage(self):
        return 0.1 + sum([x.experience / 100 for x in self.operators])

    def damaged(self, damage):
        self.health -= damage * 60 / 100
        operators = [operator for operator in self.operators
                     if operator.is_alive()]
        operators.pop(
            random.randint(0, len(operators)-1)).health -= damage * 20 / 100
        for x in operators:
            x.health -= damage * 10 / 100

    def is_alive(self) -> bool:
        return any(operator.is_alive() for operator in self.operators) \
               and super().is_alive()
