from typing import Dict, List, Literal, Optional
from numbers import Number
from time import time as timestamp

from src.base.base_data_feeder import BaseDataFeeder
from src.base.base_timer import BaseTimer
from src.timers import AcceleratedTimer
from src.exceptions import SimFinished

class ConnectedDataFeeder(BaseDataFeeder):
    def time(self) -> float:
        return timestamp()

    def get(self) -> Dict:
        pass