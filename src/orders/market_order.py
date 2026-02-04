from dataclasses import dataclass
from typing import Literal

from src.base import BaseOrder


class MarketOrder(BaseOrder):
    def __init__(self, count: int, side: Literal["buy", "sell"]):
        if not (side in ["buy", "sell"]):
            raise ValueError("sdie must be one of 'buy', 'sell'")

        self.count = count
        self.side = side
        self.price = 100 if side == "buy" else 0
