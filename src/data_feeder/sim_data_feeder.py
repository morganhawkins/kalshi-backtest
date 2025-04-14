from typing import Dict, List, Literal, Optional
from numbers import Number
from collections import deque

from src.base.base_data_feeder import BaseDataFeeder
from src.base.base_timer import BaseTimer
from src.timers import AcceleratedTimer
from src.exceptions import SimFinished

# TODO: timer abstraction to allow for fast-forwarding

class SimDataFeeder(BaseDataFeeder):
    """
    Object to simulate data realization

    Attributes:
        sim_start(float): start time (unix timestamp) of when `SimDataFeeder.start` was called
    """
    
    def __init__(self, 
                 history_start: Number, 
                 history_end: Number, 
                 history_ds: Dict[Literal["time","value"], List[Number]],
                 timer: Optional[BaseTimer]=None):
        super().__init__()
        # valdiating input types and values
        self._validate_args(history_start, history_end, history_ds, timer)
        
        # defining simulation timestamp window
        self._history_start = history_start
        self._history_end = history_end

        # storing historical data 
        self.time_history = deque(history_ds['time'])
        self.value_history = deque(history_ds['value'])

        # timer config
        if timer is None:
            # defualt behavior
            self._timer = AcceleratedTimer(1)
        else:
            self._timer = timer

        # default init values 
        self._sim_start = None
        self._last_time = None
        self._last_value = None
        self._next_time = None
        self._next_value = None

    def _validate_args(self, 
                       history_start: Number, 
                       history_end: Number, 
                       history_ds: Dict[Literal["time","value"], List[Number]],
                       timer: BaseTimer) -> bool:
        # type checks
        if not isinstance(history_start, Number) or not isinstance(history_end, Number):
            raise TypeError("`history_start` and `history_end` must be Numbers")
        if not isinstance(history_ds, Dict):
            raise TypeError("`history_ds` must be a dictionary")
        if not all(isinstance(arr, List) for arr in history_ds.values()):
            raise TypeError("all values of `history_ds` must be lists")
        if not isinstance(timer, BaseTimer):
            raise TypeError("`timer` must be a subclass of `BaseTimer`")
        
        # value checks
        if not ('value' in history_ds and 'time' in history_ds):
            raise ValueError("'value' and 'time' must both be keys in `history_ds`")
        if history_start > history_end:
            raise ValueError("`history_start` must be less than `history_end`")
        if len(history_ds['time']) != len(history_ds['value']):
            raise ValueError("time and value lists must be of the same length")

    @property
    def sim_start(self) -> float:
        if not (self._sim_start is None):
            return self._sim_start
        else:
            raise ValueError("Must start simulation with")
    
    @sim_start.setter
    def sim_start(self, value: float) -> None:
        if self._sim_start is None:
            # if has not been set yet, set sim start time
            self._sim_start = value
        else:
            # if it has been set before, raise error
            raise Exception("Sim already started, cannot start again")
    
    def _refresh(self):
        """Refreshes current time and value to be

        Raises:
            SimFinished: if out of data points
        """
        self._last_time = self._next_time
        self._last_value = self._next_value

        # popping next (time, price) off of time series
        try: 
            self._next_time = self.time_history.popleft()
            self._next_value = self.value_history.popleft()
        except IndexError:
            raise SimFinished("Simulation Finished")
    
    def start(self) -> None:
        """Begins the simualtion of data collection
        """
        self.sim_start = self._timer.time()
        self._next_time = self.time_history.popleft()
        self._next_value = self.value_history.popleft()
    
    def time(self) -> float:
        # time change since sim start
        delta_time = self._timer.time() - self.sim_start
        # add time change to history start
        sim_time = delta_time + self._history_start

        return sim_time
        
    def get(self) -> Dict[str, Number]:
        """Gets current data point
        """
        sim_time = self.time()

        # if new data available in simulation time, update until not true
        while self._next_time <= sim_time:
            self._refresh()
            
        return self._last_value


