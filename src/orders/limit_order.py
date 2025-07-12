from dataclasses import dataclass

from src.base import BaseOrder

# TODO: does this make sense to have as an object or does it need to see market to be valid
@dataclass
class LimitOrder(BaseOrder):
    pass
