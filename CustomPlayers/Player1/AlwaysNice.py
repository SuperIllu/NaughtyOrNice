import logging

from base.GameStates import Play
from base.PlayerBase import PlayerBase


class AlwaysNice(PlayerBase):
    """
    A player which always plays nice
    """

    def play(self, round_idx: int) -> Play:
        return Play.Nice

    def on_init(self):
        logging.info("Always nice created")
