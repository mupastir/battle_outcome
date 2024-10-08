import pytest
from models.units import Soldier, Vehicle

RECHARGE_MIN = 100
OPERATORS_NUMBER = 3
RECHARGE_VEHICLE = 1000
MAX_DAMAGE = 600
MAX_EXPERIENCE = 50
DAMAGE_MIN = 50
DAMAGE_AVG = 167


class TestUnits:

    def test_creating_normal_soldier(self):
        soldier = Soldier(RECHARGE_MIN)
        assert isinstance(soldier, Soldier)

    def test_creating_normal_vehicle(self):
        operators = [Soldier(RECHARGE_MIN) for x in range(OPERATORS_NUMBER)]
        vehicle = Vehicle(RECHARGE_VEHICLE, operators)
        assert isinstance(vehicle, Vehicle)

    def test_creating_soldier_with_string_recharge(self):
        with pytest.raises(TypeError):
            Soldier('')

    def test_creating_vehicle_with_string_recharge(self):
        operators = [Soldier(RECHARGE_MIN) for x in
                     range(OPERATORS_NUMBER)]
        with pytest.raises(TypeError):
            Vehicle((0,), operators)

    def test_soldier_up_experience(self, soldier: Soldier):
        experience_before = soldier.experience
        soldier.up_experience()
        assert (soldier.experience - experience_before) > 0
        assert isinstance(soldier.experience, int)

    def test_soldier_not_up_experience(self, soldier: Soldier):
        soldier.experience = MAX_EXPERIENCE
        soldier.up_experience()
        assert soldier.experience == MAX_EXPERIENCE

    def test_soldier_attack_success(self, soldier: Soldier):
        assert isinstance(soldier.attack_success, float)

    def test_soldier_attack_not_success(self, soldier: Soldier):
        soldier.damaged(MAX_DAMAGE)
        assert soldier.attack_success == 0

    def test_soldier_damage(self, soldier: Soldier):
        damage_before = soldier.damage
        soldier.up_experience()
        assert (soldier.damage - damage_before) > 0
        assert isinstance(soldier.damage, float)

    def test_soldier_get_damage(self, soldier: Soldier):
        health_before = soldier.health
        soldier.damaged(DAMAGE_MIN)
        assert health_before != soldier.health

    def test_soldier_is_alive(self, soldier: Soldier):
        is_alive_before_damage = soldier.is_alive()
        soldier.damaged(MAX_DAMAGE)
        assert not soldier.is_alive()
        assert is_alive_before_damage

    def test_vehicle_attack_success(self, vehicle: Vehicle):
        assert vehicle.attack_success != 0
        assert isinstance(vehicle.attack_success, float)

    def test_vehicle_attack_not_success(self, vehicle: Vehicle):
        vehicle.damaged(MAX_DAMAGE)
        assert vehicle.attack_success == 0

    def test_vehicle_up_experience(self, vehicle: Vehicle):
        experience_before = [operator.experience
                             for operator in vehicle.operators]
        vehicle.up_experience()
        experience_after = [operator.experience
                            for operator in vehicle.operators]
        experience = zip(experience_before, experience_after)
        for b, a in experience:
            assert (a - b) > 0

    def test_vehicle_damaged(self, vehicle: Vehicle):
        health_before = [operator.health
                         for operator in vehicle.operators]
        vehicle.damaged(300)
        health_after = [operator.health
                        for operator in vehicle.operators]
        health = zip(health_before, health_after)
        for b, a in health:
            assert b > a

    def test_vehicle_damage(self, vehicle: Vehicle):
        damage_before = vehicle.damage
        vehicle.up_experience()
        assert (vehicle.damage - damage_before) > 0
        assert isinstance(vehicle.damage, float)

    def test_vehicle_is_alive(self, vehicle: Vehicle):
        is_alive_before_damage = vehicle.is_alive()
        vehicle.damaged(MAX_DAMAGE)
        assert not vehicle.is_alive()
        assert is_alive_before_damage

    def test_vehicle_recharge_less(self):
        operators = [Soldier(RECHARGE_MIN) for x in range(OPERATORS_NUMBER)]
        with pytest.raises(ValueError):
            Vehicle(RECHARGE_MIN, operators)

    def test_vehicle_operators_less(self):
        operators = [Soldier(RECHARGE_MIN) for x in range(OPERATORS_NUMBER-1)]
        with pytest.raises(ValueError):
            Vehicle(RECHARGE_VEHICLE, operators)
