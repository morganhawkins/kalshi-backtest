from typing import List
from numbers import Number
from collections import deque
from time import time

from src.exceptions import TimerFinished
from src.base.base_timer import BaseTimer

class JumpTimer(BaseTimer):
    """
    Timer that allows for 

    Attributes:
        ratio (float): Flaot in (0,inf). Ratio of simulated speed to real speed
    """
    def __init__(self, steps: List[Number]):
        if not isinstance(steps, List):
            raise TypeError("`steps` must be a list")

        self._steps = deque(steps)
        self._curr_time = None
    
    @property
    def curr_time(self) -> Number:
        if self._curr_time is None:
            raise TimerFinished("No initial cycle, or out of time steps")
        return self._curr_time
    
    def cycle(self) -> None:
        try:
            self._curr_time = self._steps.popleft()
        except IndexError:
            self._curr_time = None 
            raise TimerFinished("no more time steps to return")

    def time(self) -> Number: 
        return self.curr_time