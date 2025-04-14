from time import time as timestamp
from numbers import Number

from src.base.base_timer import BaseTimer

class AcceleratedTimer(BaseTimer):
    """
    Timer that allows for 

    Attributes:
        ratio (float): Flaot in (0,inf). Ratio of simulated speed to real speed
    """
    def __init__(self, ratio: float=1.0):
        """_summary_

        Args:
            ratio (float, optional): Ratio of simulated time delta to real time delta. Defaults to 1.0.
        """
        self.ratio = ratio

        self._start_time = timestamp()
    
    @property
    def curr_time(self) -> Number:
        return self.time()
    
    def cycle(self) -> None:
        pass

    def time(self) -> Number:
        time_delta = timestamp() - self._start_time
        sim_time_delta = time_delta * self.ratio
        
        return sim_time_delta