from typing import Iterable, List

from models.squads import Squad
from utils import MinSquadsException


class Army:
    MIN_SQUADS_PER_ARMY = 2

    def __init__(self, squads: Iterable[Squad]):
        super().__init__()
        self.squads = list(squads)

    @property
    def squads(self) -> List[Squad]:
        return self._squads

    @squads.setter
    def squads(self, value: List[Squad]):
        self.validate_squads(value)
        self._squads = value

    def validate_squads(self, squads: List[Squad]):
        if len(squads) < self.MIN_SQUADS_PER_ARMY:
            raise MinSquadsException

    @property
    def is_active(self):
        return any([squad.is_active() for squad in self.squads])
