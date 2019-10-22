import logging

from models.armies import Army
from simulation import (RandomStrategy, Simulation, StrongestStrategy,
                        WeakestStrategy)

MAX_DAMAGE = 6000
ARMIES_SQUADS = {'test1': [5, 5], 'test2': [5, 5]}
logger = logging.getLogger(__name__)


class TestSimulation:

    def test_create_simulation(self):
        simulation = Simulation(ARMIES_SQUADS)
        assert isinstance(simulation, Simulation)
        assert isinstance(simulation.armies[-1], Army)
        assert isinstance(simulation.armies[0], Army)

    def test_simulation_running_with_strongest_strategy(self, simulation):
        army_name, attacking_damage = simulation.run(StrongestStrategy())
        assert attacking_damage >= 0
        assert isinstance(attacking_damage, float)
        assert isinstance(army_name, str)

    def test_simulation_running_with_weakest_strategy(self, simulation):
        army_name, attacking_damage = simulation.run(WeakestStrategy())
        assert attacking_damage >= 0
        assert isinstance(attacking_damage, float)
        assert isinstance(army_name, str)

    def test_simulation_running_with_random_strategy(self, simulation):
        army_name, attacking_damage = simulation.run(RandomStrategy())
        assert attacking_damage >= 0
        assert isinstance(attacking_damage, float)
        assert isinstance(army_name, str)

    def test_all_armies_alive(self, simulation):
        assert not simulation.is_only_one_army_alive

    def test_no_winner_army_yet(self, simulation):
        assert simulation.get_winner_army() is None

    def test_army_win(self, simulation_unequal):
        lost_army = simulation_unequal.armies[-1]
        [squad.damaged(MAX_DAMAGE) for squad in lost_army.squads]
        assert isinstance(simulation_unequal.get_winner_army(), str)

    def test_army_win_simulating(self, simulation):
        while not simulation.is_only_one_army_alive:
            simulation.run(RandomStrategy())
        assert isinstance(simulation.get_winner_army(), str)
