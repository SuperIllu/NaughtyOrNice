import random
from base.GameStates import Play
from base.PlayerBase import PlayerBase


class P1AlwaysRandom(PlayerBase):
    """
    A player which always flips a coin (random)
    """

    def on_init(self):
        self._random = random.Random()

    def play(self, round_idx: int) -> Play:
        roll = self._random.randint(0, 100)
        return Play.Nice if roll < 50 else Play.Naughty


class P2AlwaysRandom(PlayerBase):
    """
    A player which always flips a coin (pseudo-random)
    """

    def on_init(self):
        self._random = random.Random(123)

    def play(self, round_idx: int) -> Play:
        roll = self._random.randint(0, 100)
        return Play.Nice if roll < 50 else Play.Naughty

