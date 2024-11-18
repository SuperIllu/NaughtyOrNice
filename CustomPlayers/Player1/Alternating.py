import random
from base.GameStates import Play
from base.PlayerBase import PlayerBase


class Alternating(PlayerBase):
    """
    A player which always changes his mind
    """

    def on_init(self):
        self._last_play = Play.Naughty

    def play(self, round_idx: int) -> Play:
        if self._last_play == Play.Naughty:
            self._last_play = Play.Nice
        elif self._last_play == Play.Nice:
            self._last_play = Play.Naughty
        return self._last_play



