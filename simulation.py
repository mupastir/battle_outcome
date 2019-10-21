import logging
import random
from typing import Dict, List

from factories.squad_factory import SquadFactory
from models.armies import Army
from models.squads import Squad

logger = logging.getLogger(__name__)


def is_attacking_win(attacking_squad: Squad, defending_squad: Squad):
    return attacking_squad.attack_probability \
           > defending_squad.attack_probability


def attack_general(squad, defending_squad):
    if is_attacking_win(squad, defending_squad):
        damage = squad.damage
        defending_squad.damaged(damage)
        logger.info(f'\nAttacking squad has damaged {damage} '
                    f'points defending one!')
    else:
        logger.info('\nAttacking squad not stronger than defending,'
                    'no damage is dealt to either side.')


def random_strategy(squad: Squad, army: Army):
    defend_squad = random.choice(army.squads)
    attack_general(squad, defend_squad)


def weakest_strategy(squad: Squad, army: Army):
    defend_squad = min(army.squads)
    attack_general(squad, defend_squad)


def strongest_strategy(squad: Squad, army: Army):
    defend_squad = max(army.squads)
    attack_general(squad, defend_squad)


ATTACK_STRATEGIES = {1: random_strategy,
                     2: weakest_strategy,
                     3: strongest_strategy}


def input_number(string_explanation: str) -> int:
    number = input(string_explanation)
    return validate_input(number)


def validate_input(number: str) -> int:
    try:
        return int(number)
    except TypeError:
        print('Please enter number of armies in digits!')
        input_number('Repeat enter: ')


def is_only_one_army_alive(armies_list: List[Army]) -> bool:
    return sum([_army.is_active for _army in armies_list]) == 1


def create_armies(units_per_squad: Dict) -> Dict:
    armies_dict = {}
    for army_name, squads in units_per_squad.items():
        armies_dict[army_name] = Army(
            army_name,
            [SquadFactory(units).create() for units in squads]
        )
    return armies_dict


if __name__ == '__main__':
    armies_number = input_number('Enter the number of armies: ')
    squads_per_army = []
    units_per_squad = {}
    for _army in range(armies_number):
        number_of_squads = input_number(f'Enter the number of squads '
                                        f'for No{_army + 1} army: ')
        squads_per_army.append(number_of_squads)
    for _army in range(len(squads_per_army)):
        armies_name = input(f'Enter name of the No{_army + 1} army: ')
        units_per_squad[armies_name] = [
            input_number(f'Enter number of units for #{n + 1} '
                         f'squad for #{_army + 1} army: ')
            for n in range(squads_per_army[_army])]

    armies = create_armies(units_per_squad)

    keys = list(armies.keys())
    random.shuffle(keys)

    shuffled_dict = dict()
    for key in keys:
        shuffled_dict.update({key: armies[key]})
    my_army, enemy_army = (army for army in shuffled_dict.values())

    while not is_only_one_army_alive(list(armies.values())):
        strategy = input_number(
            f'Please, choose strategy for army\n'
            f'1 - random\n2 - weakest\n3 - strongest: ')
        for squad_n in range(len(my_army.squads)):
            attack = ATTACK_STRATEGIES.get(strategy)
            attack(my_army.squads[squad_n], enemy_army)
        my_army, enemy_army = enemy_army, my_army
