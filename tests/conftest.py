import pytest
from units import Soldier, Vehicle

RECHARGE_MIN = 100
RECHARGE_VEHICLE = 1000
RECHARGE_ANOMALY = 50000
OPERATORS_NUMBER = 3
OPERATORS_NOT_ENOUGH = 1
OPERATORS_TOO_MANY = 5


@pytest.fixture
def soldier():
    test_soldier = Soldier(RECHARGE_MIN)
    return test_soldier


@pytest.fixture
def vehicle():
    operators = [Soldier(RECHARGE_MIN) for x in range(OPERATORS_NUMBER)]
    test_vehicle = Vehicle(RECHARGE_VEHICLE, operators)
    return test_vehicle
