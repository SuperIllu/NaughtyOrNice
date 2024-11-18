import abc
from abc import abstractproperty


class PlayerBase(abc.ABC):
    """
    The abstract base class for all players
    """

    def __init__(self, manager):
        self.Manager = manager
        self.on_init()

    def on_init(self):
        pass

    @abc.abstractmethod
    def play(self, round_idx: int):
        pass

"""
    @abc.abstractmethod
    def update_result(self, round: int, result):
        pass
"""