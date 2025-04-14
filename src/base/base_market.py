from abc import ABC, abstractmethod
from typing import Literal, Dict

from src.base import BaseDataFeeder
from src.exceptions import LiquidityError, IllegalOrderError

class BaseMarket(ABC):
    """Base class for a market object. A this is meant to represent a market for a specific
    contract (specific date and expiration).

    Attributes:
        position (int): number of contracts held
    """

    def __init__(self, 
                 data_feeder: BaseDataFeeder,
                 strike: int,
                 expiration: float,
                 resolution: Literal[0,1],
                 allow_short: bool=True,
                 max_pos: int=None):
        """_summary_

        Args:
            data_feeder (BaseDataFeeder): data_feeder.get must return a dict with "bid" and "ask" as keys
            allow_short (bool): whether allowed to have a negative position
            max_pos (int): the largest absolute position allowed to take
        """
        # storing args passed
        self._data_feeder = data_feeder
        self._strike = strike
        self._expiration = expiration
        self._resolution = resolution
        self._allow_short = allow_short
        self._max_pos = max_pos

        # init to defualt values
        self._position = 0  
        self._orders = []

    @property
    def position(self) -> int:
        return self.position
    
    @property
    def tte(self) -> float:
        return self._expiration - self._data_feeder.time()
    
    @abstractmethod
    def market_order(self, contracts: int, side: Literal["buy", "sell"]) -> float:
        """places a market order, returns total cost to execute

        Args:
            contracts (int): number of contracts
            side (Literal["buy", "sell"]): side to take order on

        Raises:
            LiquidityError: if there is no limit order available to take
            IllegalOrderError: if order is now allowed (position size or direction)
            ExpiredMarketError: if market is expired

        Returns:
            (float): cash flow to your account. (negative if buying, positive if selling)
        """
    @abstractmethod
    def limit_order(self, contracts: int, side: Literal["buy", "sell"]) -> float:
        """places a limit order, returns total cost to execute. Will execute at best possible price

        Args:
            contracts (int): number of contracts
            side (Literal["buy", "sell"]): side to take order on

        Raises:
            LiquidityError: if there is no limit order available to take
            IllegalOrderError: if order is not allowed (position size or direction)
            ExpiredMarketError: if market is expired

        Returns:
            (float): cash flow to your account. (negative if buying, positive if selling)
        """
    @abstractmethod
    def fill_open_orders(self) -> None:
        """Fill orders based on retrieved data 

        Raises:
            ExpiredMarketError: if market is expired
        """
    
    @abstractmethod
    def liquidate(self) -> None:
        """liquidate position in market
        """

    def position_value(self, method: Literal["bid", "ask", "mid", "auto"]="auto"):
        """returns value of position

        Args:
            method (Literal["bid", "ask", "mid", "auto"], optional): method ot calc value when market live. Defaults to "auto".

        Raises:
            ValueError: method is not one of "bid", "ask", "mid", "auto"

        Returns:
            float: value of position
        """
        if self.tte < 0:
            return self._resolution
        
        market = self._data_feeder.get()

        if method == "auto":
            method = "bid" if self.position > 0 else "ask" 

        if method in ["bid", "ask"]:
            contract_value = market[method]
        elif method == "mid":
            contract_value = (market["bid"] + market["ask"])/2
        else:
            raise ValueError("method must be one of 'bid', 'ask', 'mid', 'auto'")
        
        return contract_value*self.position
    
    # TODO: Should this just fill orders whenever a new datapoint is requested. Does this make sense?
    # TODO: Should market just be an API/seperate_process that constantly loops and tracks orders?
    # TODO: How would one track time with this? Maybe feeder has an update time param that returns all data skipped over?
    # TODO: What if agents consume data through the market so that they have to fill orders whenever new data is requested?
    # TODO: This relies on agent requesting data frequently enough?
    # TODO: New object that holds market and timer and data feeder. Fills orders whenever timer is incremented with `timer.cycle` method
    def get_data(self) -> Dict:
        data = self._data_feeder.get() 
        self.fill_open_orders()
        return data

