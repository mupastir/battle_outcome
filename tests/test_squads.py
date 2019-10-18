import pytest
from models.squads import Squad
from models.units import Soldier
from utils import UnitsNumber

UNITS_NUMBER = 7
RECHARGE_MIN = 100
UNITS_NOT_ENOUGH = 3
MAX_DAMAGE = 10000


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

    def test_squad_attack_probability(self, squad: Squad):
        attack_probability_before = squad.attack_probability
        squad.damaged(MAX_DAMAGE)
        assert attack_probability_before != 0
        assert squad.attack_probability == 0

    def test_squad_damage(self, squad: Squad):
        damage_before = squad.damage
        assert (squad.damage - damage_before) > 0
        assert isinstance(squad.damage, float)

    def test_squad_is_active(self, squad: Squad):
        active_before_damage = squad.is_active
        squad.damaged(MAX_DAMAGE)
        active_after_damage = squad.is_active
        assert not active_after_damage
        assert active_before_damage
