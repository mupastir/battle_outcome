import pytest
from squads import Squad
from units import Soldier
from utils import UnitsNumber

UNITS_NUMBER = 7
RECHARGE_MIN = 100
UNITS_NOT_ENOUGH = 3
MAX_DAMAGE = 600


class TestSquads:

    def test_creating_normal_squad(self):
        units = [Soldier(RECHARGE_MIN) for x in range(UNITS_NUMBER)]
        squad = Squad(units)
        assert isinstance(squad, Squad)
        assert isinstance(squad.units, list)

    def test_error_creating_squad(self):
        units = [Soldier(RECHARGE_MIN) for x in range(UNITS_NOT_ENOUGH)]
        with pytest.raises(UnitsNumber):
            Squad(units)

    def test_squad_attack_probability(self, squad):
        attack_probability_before = squad.attack_probability
        squad.damaged(MAX_DAMAGE)
        assert attack_probability_before != 0
        assert squad.attack_probability == 0
