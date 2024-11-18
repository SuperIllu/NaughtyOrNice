from typing import List, Dict, Optional

from base.GameStates import RoundResult, Play, get_points_for_result


class GameManager:
    def __init__(self, player1, player2, rounds: int = 200):
        from base.PlayerBase import PlayerBase
        self.Player1: PlayerBase = player1(self)
        self.Player2: PlayerBase = player2(self)
        self.Rounds = rounds

        self._last_round = -1
        self._round_results: List[RoundResult] = []

    def play_game(self) -> None:
        self._round_results.clear()
        for round_idx in range(self.Rounds):
            self.play_next_round(round_idx)
            self._last_round = round_idx

    def play_next_round(self, round_idx: int) -> None:
        player1_play = self.Player1.play(round_idx)
        player2_play = self.Player2.play(round_idx)
        self._round_results.append(RoundResult(round_idx, self.Player1, self.Player2, player1_play, player2_play))

    def get_last_round(self) -> Optional[RoundResult]:
        if self._last_round >= 0:
            return self._round_results[self._last_round]
        return None

    def get_round(self, round_idx: int) -> RoundResult:
        """

        :param round_idx: the round ID, starting at 0
        :return:
        """
        return self._round_results[round_idx] if round_idx < len(self._round_results) else None

    def get_rounds_played(self) -> int:
        return self._last_round

    def accum_points(self) -> Dict:
        points = {type(self.Player1): 0, type(self.Player2): 0}
        for round_result in self._round_results:
            player1_res = round_result.get_result(self.Player1)
            player2_res = round_result.get_result(self.Player2)

            points[type(self.Player1)] += get_points_for_result(player1_res)
            points[type(self.Player2)] += get_points_for_result(player2_res)

        return points
