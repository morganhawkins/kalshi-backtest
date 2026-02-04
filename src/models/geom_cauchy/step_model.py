from src.base import BaseModel
from src.models.geom_cauchy import _utils


class CauchyStepModel(BaseModel):
    """Model to price and gauge risk of barrier contract using Cauchy log returns.
    In this context called 'step' contracts.
    """
    @staticmethod
    def _value(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
        return _utils.value(u_price, strike, scale, loc, tte)

    @staticmethod
    def _iv(price: float, u_price: float, strike: int, loc: float, tte: float) -> float:
        return _utils.iv(price, u_price, strike, loc, tte)

    @staticmethod
    def _delta(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
        return _utils.delta(u_price, strike, scale, loc, tte)

    @staticmethod
    def _vega(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
        return _utils.vega(u_price, strike, scale, loc, tte)

    @staticmethod
    def _theta(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
        return _utils.theta(u_price, strike, scale, loc, tte)

    @staticmethod
    def _gamma(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
        return _utils.gamma(u_price, strike, scale, loc, tte)

    @classmethod
    def __call__(
        cls,
        price: float,
        u_price: float,
        estimated_scale: float,
        estimated_loc: float,
        tte: float,
        strike: float
    ):
        iv = cls._iv(price, u_price, strike, estimated_loc, tte)
        value = cls._value(u_price, strike, estimated_scale, estimated_loc, tte)
        delta = cls._delta(u_price, strike, iv, estimated_loc, tte)
        vega = cls._vega(u_price, strike, iv, estimated_loc, tte)
        theta = cls._theta(u_price, strike, iv, estimated_loc, tte)
        gamma = cls._gamma(u_price, strike, iv, estimated_loc, tte)

        return {
            "value": value,
            "iv": iv,
            "delta": delta,
            "vega": vega,
            "theta": theta,
            "gamma": gamma
        }
