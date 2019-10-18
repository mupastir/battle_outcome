import random

from factories.unit_factories import SoldierFactory, VehiclesFactory
from models.squads import Squad


class SquadFactory:

    def __init__(self, units_number: int):
        self.units_number = units_number

    def create(self) -> Squad:
        units_factories = random.choices([SoldierFactory, VehiclesFactory],
                                         k=self.units_number)
        return Squad(
            [unit_factory.create() for unit_factory in units_factories])
