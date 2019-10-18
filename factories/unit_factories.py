from abc import ABC, abstractmethod

from models.units import Soldier, Vehicle


class UnitCreator(ABC):

    @abstractmethod
    def create(self):
        pass


class SoldierFactory(UnitCreator):

    def __init__(self, recharge=100):
        self.recharge = recharge

    def create(self) -> Soldier:
        return Soldier(self.recharge)


class VehiclesFactory(UnitCreator):
    OPERATORS_NUMBER = 3
    OPERATORS_RECHARGE = 100

    def __init__(self, recharge=1000):
        self.recharge = recharge

    def create(self) -> Vehicle:
        operators = [SoldierFactory(self.recharge).create()
                     for i in range(self.OPERATORS_NUMBER)]
        return Vehicle(self.recharge, operators)
