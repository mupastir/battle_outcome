import pytest
from factories.army_factory import ArmyFactory
from factories.squad_factory import SquadFactory
from factories.unit_factories import SoldierFactory, VehiclesFactory
from models.armies import Army
from models.squads import Squad
from models.units import Soldier, Vehicle
from utils import MinSquadsException, UnitsNumberException

RECHARGE_NORMAL = 100
RECHARGE_VEHICLE = 1000
UNITS_NUMBER = 7
MIN_UNITS_NUMBER = 2
SQUADS_NUMBER = 3
MIN_SQUADS_NUMBER = 1


class TestFactories:

    def test_create_soldier(self):
        soldier = SoldierFactory(RECHARGE_NORMAL).create()
        assert isinstance(soldier, Soldier)

    def test_create_vehicle(self):
        vehicle = VehiclesFactory(RECHARGE_VEHICLE).create()
        assert isinstance(vehicle, Vehicle)

    def test_create_squad(self):
        squad = SquadFactory(UNITS_NUMBER).create()
        assert isinstance(squad, Squad)

    def test_create_army(self):
        army = ArmyFactory(
            'test',
            [UNITS_NUMBER for i in range(SQUADS_NUMBER)]).create()
        assert isinstance(army, Army)

    def test_not_create_soldier(self):
        with pytest.raises(TypeError):
            SoldierFactory('').create()

    def test_not_create_vehicle(self):
        with pytest.raises(TypeError):
            VehiclesFactory('').create()

    def test_not_create_squad(self):
        with pytest.raises(UnitsNumberException):
            SquadFactory(MIN_UNITS_NUMBER).create()

    def test_not_create_army(self):
        with pytest.raises(MinSquadsException):
            ArmyFactory(
                'test',
                [UNITS_NUMBER for i in range(MIN_SQUADS_NUMBER)]).create()
