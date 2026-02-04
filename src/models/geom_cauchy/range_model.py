from typing import Tuple

from src.base import BaseModel
from src.models.geom_cauchy import _utils


class CauchyRangeModel(BaseModel):
    """Model to price and gauge risk of event contract using Cauchy log returns.
    In this context called 'range' contracts.
    """
    @staticmethod
    def _value(u_price: float, strike: Tuple[int, int], scale: float, loc: float, tte: float) -> float:
        lower = _utils.value(u_price, strike[0], scale, loc, tte)
        upper = _utils.value(u_price, strike[1], scale, loc, tte)
        return lower - upper

    @staticmethod
    def _iv(price: float, u_price: float, strike: Tuple[int, int], loc: float, tte: float) -> float:
        lower = _utils.iv(price, u_price, strike[0], loc, tte)
        upper = _utils.iv(price, u_price, strike[1], loc, tte)
        return lower - upper

    @staticmethod
    def _delta(u_price: float, strike: Tuple[int, int], scale: float, loc: float, tte: float) -> float:
        lower = _utils.delta(u_price, strike[0], scale, loc, tte)
        upper = _utils.delta(u_price, strike[1], scale, loc, tte)
        return lower - upper

    @staticmethod
    def _vega(u_price: float, strike: Tuple[int, int], scale: float, loc: float, tte: float) -> float:
        lower = _utils.vega(u_price, strike[0], scale, loc, tte)
        upper = _utils.vega(u_price, strike[1], scale, loc, tte)
        return lower - upper

    @staticmethod
    def _theta(u_price: float, strike: Tuple[int, int], scale: float, loc: float, tte: float) -> float:
        lower = _utils.theta(u_price, strike[0], scale, loc, tte)
        upper = _utils.theta(u_price, strike[1], scale, loc, tte)
        return lower - upper

    @staticmethod
    def _gamma(u_price: float, strike: Tuple[int, int], scale: float, loc: float, tte: float) -> float:
        lower = _utils.gamma(u_price, strike[0], scale, loc, tte)
        upper = _utils.gamma(u_price, strike[1], scale, loc, tte)
        return lower - upper

    @classmethod
    def __call__(cls, price: float, u_price: float, estimated_scale: float, estimated_loc: float, tte: float, strike: Tuple[int, int]):
        iv_lower = cls._iv(price, u_price, strike[0], estimated_loc, tte)
        iv_upper = cls._iv(price, u_price, strike[1], estimated_loc, tte)
        iv = (iv_lower + iv_upper) / 2

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
