import pytest
from models.squads import Squad
from models.units import Soldier, Vehicle

RECHARGE_MIN = 100
RECHARGE_VEHICLE = 1000
RECHARGE_ANOMALY = 50000
OPERATORS_NUMBER = 3
OPERATORS_NOT_ENOUGH = 1
OPERATORS_TOO_MANY = 5
UNITS_NUMBER = 7


@pytest.fixture
def soldier():
    test_soldier = Soldier(RECHARGE_MIN)
    return test_soldier


@pytest.fixture
def vehicle():
    operators = [Soldier(RECHARGE_MIN) for x in range(OPERATORS_NUMBER)]
    test_vehicle = Vehicle(RECHARGE_VEHICLE, operators)
    return test_vehicle


@pytest.fixture
def squad():
    return _create_squad()


@pytest.fixture
def squad_enemy():
    return _create_squad()


def _create_squad():
    units = [_create_vehicle() for x in range(UNITS_NUMBER)]
    pure_squad = Squad(units)
    return pure_squad


def _create_vehicle():
    operators = [Soldier(RECHARGE_MIN) for x in range(OPERATORS_NUMBER)]
    test_vehicle = Vehicle(RECHARGE_VEHICLE, operators)
    return test_vehicle
