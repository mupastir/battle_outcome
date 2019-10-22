import copy
import random
from abc import ABC
from typing import Dict, List

from factories.army_factory import ArmyFactory
from models.armies import Army
from models.squads import Squad


class Strategy(ABC):
    FUNCTION_SELECTOR = None

    def get_enemy_squad(self, defending: Army) -> Squad:
        return self.FUNCTION_SELECTOR(
            [squad for squad in defending.squads if squad.is_active]
        )


class RandomStrategy(Strategy):
    FUNCTION_SELECTOR = random.choice


class WeakestStrategy(Strategy):
    FUNCTION_SELECTOR = min


class StrongestStrategy(Strategy):
    FUNCTION_SELECTOR = max


class Simulation:
    MIN_ARMIES_NUMBER = 2

    def __init__(self,
                 armies_squads: Dict[str, List[int]]):
        self.armies = [ArmyFactory(army_name, units_numbers).create()
                       for army_name, units_numbers in armies_squads.items()]
        random.shuffle(self.armies)
        self.attacking_army_ind = 0

    def run(self, strategy: Strategy) -> (str, float):
        attacking_army, enemy_armies = self._get_armies()
        total_damage = 0
        for enemy_army in enemy_armies:
            for squad_n in range(len(attacking_army.squads)):
                if enemy_army.is_active:
                    enemy_squad = strategy.get_enemy_squad(enemy_army)
                    total_damage += self._attack(
                        attacking_army.squads[squad_n], enemy_squad)
        self._change_attacking_army()
        return attacking_army.name, total_damage

    def _change_attacking_army(self):
        if self.attacking_army_ind+1 < len(self.armies):
            self.attacking_army_ind += 1
        else:
            self.attacking_army_ind = 0

    def _get_armies(self) -> (Army, List[Army]):
        armies = copy.copy(self.armies)
        return armies.pop(self.attacking_army_ind), armies

    @staticmethod
    def _is_attacking_win(attacking: Squad, defending: Squad) -> bool:
        return attacking.attack_probability \
               > defending.attack_probability

    def _attack(self, attacking, defending) -> float:
        if self._is_attacking_win(attacking, defending):
            damage = attacking.damage
            defending.damaged(damage)
            return damage
        return 0.0

    def get_winner_army(self) -> [str, None]:
        if self.is_only_one_army_alive:
            return [army.name for army in self.armies if army.is_active][-1]
        return None

    @property
    def is_only_one_army_alive(self) -> bool:
        return sum([army.is_active for army in self.armies]) == 1
