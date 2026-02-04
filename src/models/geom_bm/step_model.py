from src.base import BaseModel
from src.models.geom_bm import _utils

class GBMStepModel(BaseModel):
    """Model to price and gauge risk of barrier conctract. In this 
    context called 'step' contracts.
    """
    @staticmethod
    def _value(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.value(u_price, strike, sigma, mu, tte)
    
    @staticmethod
    def _iv(price: float, u_price: float, strike: int, mu: float, tte: float) -> float:
        return _utils.iv(price, u_price, strike, mu, tte)
    
    @staticmethod
    def _delta(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.delta(u_price, strike, sigma, mu, tte)
    
    @staticmethod
    def _vega(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.vega(u_price, strike, sigma, mu, tte)
    
    @staticmethod
    def _theta(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.theta(u_price, strike, sigma, mu, tte)
    
    @staticmethod
    def _gamma(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
        return _utils.gamma(u_price, strike, sigma, mu, tte)
    
    @classmethod
    def __call__(
        cls, 
        price: float, 
        u_price: float, 
        estimated_sigma: float, 
        estimated_mu: float, 
        tte: float, 
        strike: float
    ):
        iv = cls._iv(price, u_price, strike, estimated_mu, tte)
        value = cls._value(u_price, strike, estimated_sigma, estimated_mu, tte)
        delta = cls._delta(u_price, strike, iv, estimated_mu, tte)
        vega = cls._vega(u_price, strike, iv, estimated_mu, tte)
        theta = cls._theta(u_price, strike, iv, estimated_mu, tte)
        gamma = cls._gamma(u_price, strike, iv, estimated_mu, tte)

        return {
            "value": value,
            "iv": iv,
            "delta": delta,
            "vega": vega,
            "theta": theta,
            "gamma": gamma
            }







