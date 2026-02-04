from typing import List
from numbers import Number
from collections import deque
from time import time

from src.exceptions import TimerFinished
from src.base.base_timer import BaseTimer


class DeltaTimer(BaseTimer):
    """
    Timer that allows for 

    Attributes:
        ratio (float): Flaot in (0,inf). Ratio of simulated speed to real speed
    """

    def __init__(self, delta: Number):
        if not isinstance(delta, Number):
            raise TypeError("`steps` must be a Number")
        self._delta = delta
        self._curr_time = 0

    @property
    def curr_time(self) -> Number:
        return self._curr_time

    def cycle(self) -> None:
        self._curr_time += self._delta

    def time(self) -> Number:
        return self.curr_time
