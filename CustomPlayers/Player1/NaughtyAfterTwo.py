import random
from base.GameStates import Play
from base.PlayerBase import PlayerBase


class NaughtyAfterTwo(PlayerBase):
    """
    A player which is nice unless it sees two naughties in a row
    """

    def play(self, round_idx: int) -> Play:
        if round_idx <= 2:
            return Play.Nice
        else:
            previous_round = self.Manager.get_round(round_idx-1)
            pre_previous_round = self.Manager.get_round(round_idx-2)
            opp_play_prev = previous_round.get_opponent_play(self)
            opp_play_prev_prev = pre_previous_round.get_opponent_play(self)

            if opp_play_prev == Play.Naughty and opp_play_prev_prev == Play.Naughty:
                return Play.Naughty
            else:
                return Play.Nice


