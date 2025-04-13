from time import time

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

        self._start_time = time()

    def time(self) -> float:
        time_delta = time() - self._start_time
        sim_time_delta = time_delta * self.ratio
        
        return sim_time_delta