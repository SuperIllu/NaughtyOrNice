import logging
from enum import  Enum

from base.PlayerBase import PlayerBase


class Play(Enum):
    Undef = 0
    Nice = 1
    Naughty = 2


class ResultType(Enum):
    Unplayed = 0
    Collaboration = 1
    Victory = 2
    Distrust = 3


class Result(Enum):
    """ result from the perspective of one player """
    Undef = 0
    Win = 1
    Loss = 2
    Collaboration = 3
    Distrust = 4


def get_points_for_result(result: Result):
    if result == Result.Win:
        return 5
    elif result == Result.Collaboration:
        return 3
    elif result == Result.Distrust:
        return 1
    return 0


class RoundResult:

    def __init__(self, round: int, player1: PlayerBase, player2: PlayerBase, play1: Play, play2: Play):
        self.Round: int = round
        self.Player1: PlayerBase = player1
        self.Player2: PlayerBase = player2
        self.Player1Play: Play = play1
        self.Player2Play: Play = play2

    def get_result(self, player) -> Result:
        """
        Get the result from the perspective of one player
        :param player:
        :return:
        """
        if player not in [self.Player1, self.Player2]:
            logging.error(f"{player} not playing")
            return Result.Undef

        if Play.Undef in [self.Player1Play, self.Player2Play]:
            logging.warning(f"undefined play")
            return Result.Undef

        assert (self.Player1Play in [Play.Nice, Play.Naughty])
        assert (self.Player2Play in [Play.Nice, Play.Naughty])

        if self.Player1Play == self.Player2Play:
            # both chose same behaviour
            return Result.Collaboration if self.Player1Play is Play.Nice else Result.Distrust

        # players chose differently: winner was naughty, loser was nice
        player1_won = self.Player1Play == Play.Naughty
        if player == self.Player1:
            return Result.Win if player1_won else Result.Loss
        elif player == self.Player2:
            return Result.Loss if player1_won else Result.Win

        logging.error(f"Something went wrong: {self.Player1Play}, {self.Player2Play}")
        return Result.Undef

    def get_my_play(self, player) -> Play:
        """
        What did I (player) play last round?
        :param player: me
        :return:
        """
        if player not in [self.Player1, self.Player2]:
            logging.error(f"{player} not playing")
            return Play.Undef

        if player == self.Player1:
            return self.Player1Play

        elif player == self.Player2:
            return self.Player2Play

    def get_opponent_play(self, player) -> Play:
        """
        What did my opponent play last round
        :param player: me, not the opponent
        :return:
        """
        if player not in [self.Player1, self.Player2]:
            logging.error(f"{player} not playing")
            return Play.Undef

        if player == self.Player1:
            return self.Player2Play

        elif player == self.Player2:
            return self.Player1Play
