from typing import Tuple, Union
from abc import ABC, abstractmethod


class BaseModel(ABC):
    """Abstract class to describe pricing entities. 

    Attributes:
        strike (Union[int, tuple]): int signifies step contratc strike, tuple if range with 2 srikes 
        expiration (float): unix timestamp representing contract expiration
    """

    @abstractmethod
    def _value(self, sigma: float, mu: float) -> float:
        pass

    @abstractmethod
    def _iv(self, price: float, mu: float) -> float:
        pass

    @abstractmethod
    def _delta(self, price: float, sigma: float, mu: float) -> float:
        pass

    @abstractmethod
    def _vega(self, price: float, sigma: float, mu: float) -> float:
        pass

    @abstractmethod
    def _theta(self, price: float, sigma: float, mu: float) -> float:
        pass

    @abstractmethod
    def _gamma(self, price: float, sigma: float, mu: float) -> float:
        pass
