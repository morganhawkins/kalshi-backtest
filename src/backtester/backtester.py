from src.base import BaseTimer
from src.base import BaseAgent
from src.base import BaseDataFeeder

class EventBackTester:
    """An Event is defined by Kalshi as a set of contracts that all share an 
    underlying asset and expiration but differ in strike price
    """
    def __init__(self, agent: BaseAgent, timer: BaseTimer, feeder: BaseDataFeeder):
        self._agent = agent
        self._timer = timer
        self._feeder = feeder

    def consume():



    