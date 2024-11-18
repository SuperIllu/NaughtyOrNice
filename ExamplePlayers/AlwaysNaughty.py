from base.GameStates import Play
from base.PlayerBase import PlayerBase


class AlwaysNaughty(PlayerBase):
    """
    A player which always plays naughty
    """

    def play(self, round_idx: int) -> Play:
        return Play.Naughty

