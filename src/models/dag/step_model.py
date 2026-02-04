from typing import Optional, Dict


from src.base import BaseModel
from . _utils import DAG, _build_tree

# NOTE: can probably estimate gamma vega theta numerically, but
# this will exas errors if tree is not sufficiently deep


class DAGStepModel(BaseModel):
    dag: Optional[DAG]

    def __init__(
        self,
        strike: int,
        expiration: float,
        u: float,
        depth=10,
        rate=0,
    ):
        self.strike = strike
        self.expiration = expiration
        self.u = u
        self.depth = depth
        self.rate = rate

        self.dag = None

    @staticmethod
    def _value(
        u_price: float,
        strike: float,
        u,
        depth: int
    ) -> float:
        tree = _build_tree(u_price, strike, u, depth)
        return tree.calc_node_deriv_value(rate=0)

    @staticmethod
    def _iv(*_, **__) -> float:
        raise NotImplementedError("_iv not implemnted for DAG model")

    @staticmethod
    def _delta(
        u_price: float,
        strike: float,
        u,
        depth: int
    ) -> float:
        tree = _build_tree(u_price, strike, u, depth)
        return tree.calc_node_deriv_value(rate=0)

    @staticmethod
    def _vega(*_, **__) -> float:
        raise NotImplementedError("_vega not implemnted for DAG model")

    @staticmethod
    def _theta(*_, **__) -> float:
        raise NotImplementedError("_theta not implemnted for DAG model")

    @staticmethod
    def _gamma(*_, **__) -> float:
        raise NotImplementedError("_gamma not implemnted for DAG model")

    @classmethod
    def __call__(
        cls,
        u_price: float,
        strike: float,
        u,
        depth: int
    ) -> Dict[str, float]:
        tree = _build_tree(u_price, strike, u, depth)
        iv = None
        value = tree.calc_node_deriv_value(rate=0)
        delta = tree.delta
        vega = None
        theta = None
        gamma = None

        return {
            "value": value,
            "iv": iv,
            "delta": delta,
            "vega": vega,
            "theta": theta,
            "gamma": gamma
        }
