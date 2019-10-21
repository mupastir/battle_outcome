import logging
from typing import Dict, List

from messages import (armies_number_msg, damaged_not_success, damaged_success,
                      name_army_entry_msg, number_of_squads_msg,
                      number_of_units_msg, repeat_input, uncorrected_number)

logger = logging.getLogger(__name__)


class View:

    def _input_number(self, string_explanation: str) -> int:
        number = input(string_explanation)
        return self._validate_input(number)

    @staticmethod
    def damaged_info(damage: int):
        if damage > 0:
            logging.info(damaged_success.format(damage))
        else:
            logging.info(damaged_not_success)

    def _validate_input(self, number: str) -> int:
        try:
            return int(number)
        except TypeError:
            logger.info(uncorrected_number)
            self._input_number(repeat_input)

    def _input_squads(self, number_of_squads: int) -> List[int]:
        return [self._input_number(number_of_units_msg.format(squad+1))
                for squad in range(number_of_squads)]

    def _input_army(self) -> Dict[str, List[int]]:
        name_army = input(name_army_entry_msg)
        number_of_squads = self._input_number(number_of_squads_msg)
        squads_list = self._input_squads(number_of_squads)
        return {name_army: squads_list}

    def input_armies(self) -> Dict[str, List[int]]:
        armies_dict = {}
        armies_number = self._input_number(armies_number_msg)
        for army in range(armies_number):
            armies_dict.update(self._input_army())
        return armies_dict
