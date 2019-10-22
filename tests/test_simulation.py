import logging

from models.armies import Army
from simulation import (RandomStrategy, Simulation, StrongestStrategy,
                        WeakestStrategy)

ARMIES_SQUADS = {'test1': [5, 5], 'test2': [5, 5]}
logger = logging.getLogger(__name__)


class TestSimulation:

    def test_create_simulation(self):
        simulation = Simulation(ARMIES_SQUADS)
        assert isinstance(simulation, Simulation)
        assert isinstance(simulation.armies[-1], Army)
        assert isinstance(simulation.armies[0], Army)

    def test_simulation_running_with_strongest_strategy(self, simulation):
        attacking_damage = simulation.run(StrongestStrategy)
        assert attacking_damage >= 0
        assert isinstance(attacking_damage, float)

    def test_simulation_running_with_weakest_strategy(self, simulation):
        attacking_damage = simulation.run(WeakestStrategy)
        assert attacking_damage >= 0
        assert isinstance(attacking_damage, float)

    def test_simulation_running_with_random_strategy(self, simulation):
        attacking_damage = simulation.run(RandomStrategy)
        assert attacking_damage >= 0
        assert isinstance(attacking_damage, float)

    def test_all_armies_alive(self, simulation):
        assert not simulation.is_only_one_army_alive

    def test_no_winner_army_yet(self, simulation):
        assert simulation.get_winner_army() is None

    def test_army_win(self, simulation):
        while not simulation.is_only_one_army_alive:
            logging.info([army.is_active for army in simulation.armies])
            simulation.run(WeakestStrategy)
        assert isinstance(simulation.get_winner_army(), Army)
