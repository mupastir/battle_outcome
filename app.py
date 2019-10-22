from console_user_interface import ConsoleUserInterface
from constants import ATTACK_STRATEGIES
from simulation import Simulation
from utils import MinArmiesException, MinSquadsException, UnitsNumberException


class BattleField:

    def __init__(self):
        self.user_interface = ConsoleUserInterface()
        self.simulation = self._valid_user_data()

    def run(self):
        while not self.simulation.is_only_one_army_alive:
            strategy = ATTACK_STRATEGIES.get(
                self.user_interface.get_strategy()
            )
            attacking, damage = self.simulation.run(strategy)
            self.user_interface.damaged_info(attacking, damage)
        winner_army = self.simulation.get_winner_army()
        self.user_interface.info_winner(winner_army)

    def _valid_user_data(self):
        try:
            armies = self.user_interface.get_armies()
            simulation_inner = Simulation(armies)
            return simulation_inner
        except (UnitsNumberException, MinArmiesException, MinSquadsException):
            self.user_interface.exception_warnings()
            self._valid_user_data()


def run():
    battle_field = BattleField()
    battle_field.run()


if __name__ == '__main__':
    run()
