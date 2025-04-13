from typing import Tuple, Union
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract class to describe pricing entities. 

    Attributes:
        strike (Union[int, tuple]): int signifies step contratc strike, tuple if range with 2 srikes 
        expiration (float): unix timestamp representing contract expiration
    """
    def __init__(self, strike: Union[int, Tuple], expiration: float):
        if not isinstance(expiration, (int, float)):
            raise TypeError("`expiration` must be an int or a float")

        self._strike = strike
        self._expiration = expiration

    @property
    def strike(self) -> Union[int, Tuple]:
        return self._strike

    @property
    def expiration(self) -> float:
        return self._expiration

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