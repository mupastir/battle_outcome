import logging
import sys
from typing import Dict, List

from constants import ATTACK_STRATEGIES
from messages import (armies_number_msg, attacking_msg, damaged_not_success,
                      damaged_success, exception_msg, name_army_entry_msg,
                      number_of_squads_msg, number_of_units_msg, repeat_input,
                      strategy_choose_msg, uncorrected_number, winner_msg,
                      wrong_strategy)
from utils import StrategyValue

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsoleUserInterface:

    def _input_number(self, string_explanation: str) -> int:
        number = input(string_explanation)
        return self._validate_input(number)

    @staticmethod
    def damaged_info(attacking_army: str, damage: float):
        if damage > 0:
            logging.info(damaged_success.format(attacking_army, damage))
        else:
            logging.info(damaged_not_success.format(attacking_army))

    def _validate_input(self, number: str) -> int:
        try:
            return int(number)
        except (ValueError, TypeError):
            logger.info(uncorrected_number)
            return self._input_number(repeat_input)

    def _input_squads(self, number_of_squads: int) -> List[int]:
        squad_list = []
        for squad in range(number_of_squads):
            squad_list.append(
                self._input_number(
                    number_of_units_msg.format(squad + 1)
                )
            )
        return squad_list

    def _input_army(self) -> Dict[str, List[int]]:
        name_army = input(name_army_entry_msg)
        number_of_squads = self._input_number(number_of_squads_msg)
        squads_list = self._input_squads(number_of_squads)
        return {name_army: squads_list}

    def get_armies(self) -> Dict[str, List[int]]:
        armies_dict = {}
        armies_number = self._input_number(armies_number_msg)
        for army in range(armies_number):
            armies_dict.update(self._input_army())
        return armies_dict

    def get_strategy(self) -> int:
        try:
            strategy = self._input_strategy()
            return strategy
        except StrategyValue:
            logging.info(wrong_strategy)
            return self.get_strategy()

    def _input_strategy(self) -> int:
        strategy = self._input_number(strategy_choose_msg)
        if strategy > len(ATTACK_STRATEGIES):
            raise StrategyValue
        return strategy

    @staticmethod
    def info_winner(winner: str):
        logging.info(winner_msg.format(winner))

    @staticmethod
    def exception_warnings():
        logging.info(exception_msg)

    @staticmethod
    def info_attacking(attacking: str):
        logging.info(attacking_msg.format(attacking))
