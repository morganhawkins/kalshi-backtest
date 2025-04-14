from abc import ABC, abstractmethod
from typing import Literal

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
        self._allow_short = allow_short
        self._max_pos = max_pos

        # init to defualt values
        self._position = 0  
        self._orders = []

    @property
    def position(self) -> int:
        return self.position
    
    @abstractmethod
    def market_order(self, contracts: int, side: Literal["buy", "sell"]) -> float:
        """places a market order, returns total cost to execute

        Args:
            contracts (int): number of contracts
            side (Literal["buy", "sell"]): side to take order on

        Raises:
            LiquidityError: if there is no limit order available to take
            IllegalOrderError: if order is now allowed (position size or direction)

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

        Returns:
            (float): cash flow to your account. (negative if buying, positive if selling)
        """
    
    @abstractmethod
    def liquidate(self) -> None:
        """liquidate position in market
        """

    def position_value(self, method: Literal["bid", "ask", "mid", "auto"]="auto"):
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
