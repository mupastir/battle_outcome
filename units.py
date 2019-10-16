import random
import numpy as np
from abc import ABC, abstractmethod
import typing


class BaseUnit(ABC):

    def __init__(self, recharge: int):
        super(BaseUnit, self).__init__()
        self.health = 100
        self.recharge = recharge

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def damage(self):
        pass

    @property
    def alive(self):
        if self.health <= 0:
            return False
        return True


class Soldier(BaseUnit, ABC):

    def __init__(self, recharge: int):
        super().__init__(recharge)
        self.experience = 0

    def up_experience(self, func):
        def decorated(*args):
            func(*args)
            self.experience += 1
            return

        return decorated

    def attack_success(self):
        return 0.5 * (1 + self.health / 100) * random.randint(
            50 + self.experience, 100) / 100

    def damage(self):
        return 0.05 + self.experience / 100

    def damaged(self, damage):
        self.health -= damage


class Vehicle(BaseUnit, ABC):
    OPERATORS_COUNT = 3

    def __init__(self, recharge: int, *operators: typing.Iterable[Soldier]):
        super().__init__(recharge)
        self.operators = self._get_operators(operators)
        self.total_health = self.health + (sum(self._operators_health)
                                           / len(self._operators_health))

    def _get_operators(self, operators):
        if len(operators) != self.OPERATORS_COUNT:
            raise ValueError

    @property
    def _operators_health(self):
        return [x.health for x in self.operators]

    @property
    def _geometric_avg(self, *attack_success):
        a = np.array(attack_success)
        return a.prod() ** (1.0 / len(a))

    def attack(self):
        return (0.5 * (1 + self.health / 100)
                * self._geometric_avg(
                    [x.attack_success for x in self.operators]))

    def damage(self):
        return 0.1 + sum([x.experience / 100 for x in self.operators])

    def damaged(self, damage):
        self.health -= damage * 60 / 100
        operators = self.operators
        operators.pop([random.randint(0, 3)]).health -= damage * 20 / 100
        for x in operators:
            x.health -= damage * 10 / 100
