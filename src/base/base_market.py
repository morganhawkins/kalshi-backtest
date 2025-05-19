from abc import ABC, abstractmethod
from typing import Literal, Dict, List
from numbers import Number

from src.base.base_data_feeder import BaseDataFeeder
from src.base.base_order import BaseOrder
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
        self._position: int = 0  
        self._cash: float = 0
        self._orders: List[BaseOrder] = []

    @property
    def position(self) -> int:
        return self._position
    
    @property
    def tte(self) -> float:
        return self._expiration - self._data_feeder.time()
    
    @abstractmethod
    def market_order(self, contracts: int, side: Literal["buy", "sell"]) -> None:
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
        pass

    @abstractmethod
    def limit_order(self, contracts: int, side: Literal["buy", "sell"], price: Number) -> None:
        """places a limit order, returns total cost to execute. Will execute at best possible price

        Args:
            contracts (int): number of contracts
            side (Literal["buy", "sell"]): side to take order on
            price (Number): price to place limit order at

        Raises:
            LiquidityError: if there is no limit order available to take
            IllegalOrderError: if order is not allowed (position size or direction)
            ExpiredMarketError: if market is expired

        Returns:
            (float): cash flow to your account. (negative if buying, positive if selling)
        """
        pass
    
    @abstractmethod
    def liquidate(self) -> None:
        """liquidate position in market
        """
        pass

    @abstractmethod
    def remove_orders(self, side=None, price=None):
        """remove orders
        """
        pass
    
    @abstractmethod
    def clear_orders(self) -> None:
        """removes all limit orders
        """
        pass

    def position_value(self, method: Literal["bid", "ask", "mid", "auto"]="auto"):
        """returns value of position

        Args:
            method (Literal["bid", "ask", "mid", "auto"], optional): method ot calc value when market live. Defaults to "auto".

        Raises:
            ValueError: method is not one of "bid", "ask", "mid", "auto"

        Returns:
            float: value of position
        """
        
        market = self._data_feeder.get()

        if method == "auto":
            method = "bid" if self.position > 0 else "ask" 

        if method in ["bid", "ask"]:
            contract_value = market[method]
        elif method == "mid":
            contract_value = (market["bid"] + market["ask"])/2
        else:
            raise ValueError("method must be one of 'bid', 'ask', 'mid', 'auto'")
        
        print("contract_value:",contract_value)
        
        return contract_value*self.position + self._cash
    

    def get_data(self) -> Dict:
        data = self._data_feeder.get()
        return data
    


