import random
from abc import ABC, abstractmethod
from typing import Dict, List

from factories.army_factory import ArmyFactory
from models.armies import Army
from models.squads import Squad


class Strategy(ABC):
    @abstractmethod
    def get_enemy_squad(self, defending: Army) -> Squad:
        pass


class RandomStrategy(Strategy):
    def get_enemy_squad(self, defending: Army) -> Squad:
        return random.choice(defending.squads)


class WeakestStrategy(Strategy):
    def get_enemy_squad(self, defending: Army) -> Squad:
        return min(defending.squads)


class StrongestStrategy(Strategy):
    def get_enemy_squad(self, defending: Army) -> Squad:
        return max(defending.squads)


ATTACK_STRATEGIES = {1: RandomStrategy,
                     2: WeakestStrategy,
                     3: StrongestStrategy}


class Simulation:
    MIN_ARMIES_NUMBER = 2

    def __init__(self,
                 armies_squads: Dict[str, List[int]]):
        self.armies = [ArmyFactory(army_name, units_numbers).create()
                       for army_name, units_numbers in armies_squads.items()]
        self.my_army, self.enemy_army = self.armies[0], self.armies[1]

    def run(self, strategy: Strategy) -> str:
        while not self._is_only_one_army_alive():
            for squad_n in range(len(self.my_army.squads)):
                enemy_squad = strategy.get_enemy_squad(self.enemy_army)
                self.attack(self.my_army.squads[squad_n], enemy_squad)
            self.my_army, self.enemy_army = self.enemy_army, self.my_army
        return [army.name for army in self.armies if army.is_active][-1]

    @staticmethod
    def is_attacking_win(attacking: Squad, defending: Squad):
        return attacking.attack_probability \
               > defending.attack_probability

    def attack(self, squad, defending_squad):
        if self.is_attacking_win(squad, defending_squad):
            damage = squad.damage
            defending_squad.damaged(damage)
            return damage
        return 0

    def _is_only_one_army_alive(self) -> bool:
        return sum([army.is_active for army in self.armies]) == 1
