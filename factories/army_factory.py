from typing import Iterable

from factories.squad_factory import SquadFactory
from models.armies import Army


class ArmyFactory:

    def __init__(self, army_name: str, unit_number: Iterable[int]):
        self.units_number = unit_number
        self.army_name = army_name

    def create(self) -> Army:
        return Army(
            self.army_name,
            [SquadFactory(units_number).create()
             for units_number in self.units_number]
        )
