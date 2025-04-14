from typing import Tuple

import numpy as np
import scipy as sp

from src.base import BaseModel

class GBMRangeModel(BaseModel):
    def __init__(self, strike: Tuple, expiration: float):
        super().__init__(strike, expiration)

        if not isinstance(strike, Tuple):
            raise TypeError("`strike` must be a tuple for range contracts")
        
    def _value(self, sigma: float, mu: float) -> float:
        pass

    def _iv(self, price: float, mu: float) -> float:
        pass

    def _delta(self, price: float, sigma: float, mu: float) -> float:
        pass

    def _vega(self, price: float, sigma: float, mu: float) -> float:
        pass

    def _theta(self, price: float, sigma: float, mu: float) -> float:
        pass

    def _gamma(self, price: float, sigma: float, mu: float) -> float:
        pass

