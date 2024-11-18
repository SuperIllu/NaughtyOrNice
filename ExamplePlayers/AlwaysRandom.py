import random
from base.GameStates import Play
from base.PlayerBase import PlayerBase


class AlwaysRandom(PlayerBase):
    """
    A player which always plays nice
    """

    def on_init(self):
        self._random = random.Random()

    def play(self, round_idx: int) -> Play:
        roll = self._random.randint(0, 100)
        return Play.Nice if roll < 50 else Play.Naughty

