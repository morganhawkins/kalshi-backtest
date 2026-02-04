from dataclasses import dataclass
from numbers import Number
from typing import Literal


@dataclass
class BaseOrder():
    side: Literal["buy", "sell"]
    price: Number
    count: int

    def fill_cash_flow(self, price: Number) -> Number:
        side = -1 if self.side == "buy" else 1

        return side * price * self.count

    def fill_contract_flow(self) -> int:
        side = 1 if self.side == "buy" else -1

        return side * self.count

    def fill_price(self, price: Number) -> Number:
        if self.side == "buy":
            return min(price, self.price)
        elif self.side == "sell":
            return max(price, self.price)
        else:
            raise Exception("Order.side not in 'buy', 'sell'")
