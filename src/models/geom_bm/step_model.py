from typing import Tuple

import numpy as np
from scipy.special import erf as erf
from scipy.special import erfinv as erfinv

from src.base import BaseModel
from src.models.geom_bm import _utils

class GBMStepModel(BaseModel):
    """Model to price and gauge risk of barrier conctract. In this 
    context called 'step' contracts.

    Attributes:
        strike (int): contract strike price in usd
        expiration (float): unix timestamp representing contract expiration

    """
    def __init__(self, strike: int, expiration: float):
        super().__init__(strike, expiration)

        if not isinstance(strike, int):
            raise TypeError("`strike` must be an int for step contracts")
        
    def _value(self, u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.value(u_price, strike, sigma, mu, tte)
    
    def _iv(self, price: float, u_price: float, strike: int, mu: float, tte: float) -> float:
        return _utils.iv(price, u_price, strike, mu, tte)

    def _delta(self, u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.delta(u_price, strike, sigma, mu, tte)

    def _vega(self, u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.vega(u_price, strike, sigma, mu, tte)

    def _theta(self, u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.theta(u_price, strike, sigma, mu, tte)

    def _gamma(self, u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.gamma(u_price, strike, sigma, mu, tte)
    
    def __call__(self, price: float, u_price: float, estimated_sigma: float, estimated_mu: float, tte: float):
        iv = self._iv(price, u_price, self.strike, estimated_mu, tte)
        value = self._value(u_price, self.strike, estimated_sigma, estimated_mu, tte)
        delta = self._delta(u_price, self.strike, estimated_sigma, estimated_mu, tte)
        vega = self._vega(u_price, self.strike, estimated_sigma, estimated_mu, tte)
        theta = self._theta(u_price, self.strike, estimated_sigma, estimated_mu, tte)
        gamma = self._gamma(u_price, self.strike, estimated_sigma, estimated_mu, tte)

        return {
            "value": value,
            "iv": iv,
            "delta": delta,
            "vega": vega,
            "theta": theta,
            "gamma": gamma
            }







