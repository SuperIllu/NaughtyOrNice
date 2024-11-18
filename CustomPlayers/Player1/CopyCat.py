import random
from base.GameStates import Play
from base.PlayerBase import PlayerBase


class CopyCat(PlayerBase):
    """
    A player which copies the other one's behaviour
    """

    def play(self, round_idx: int) -> Play:
        if round_idx == 0:
            return Play.Nice
        else:
            previous_round = self.Manager.get_last_round()
            return previous_round.get_opponent_play(self)


