from typing import Literal, Dict
from numbers import Number

from src.base import BaseMarket, BaseTimer, BaseDataFeeder, BaseOrder
from src.orders import LimitOrder, MarketOrder
from src.exceptions import SimFinished


class SimKalshiMarket(BaseMarket):
    def __init__(self,
                 timer: BaseTimer,
                 data_feeder: BaseDataFeeder,
                 strike: int,
                 expiration: float,
                 resolution: Literal[0, 1],
                 allow_short: bool = True,
                 max_pos: int = None):
        super().__init__(data_feeder, strike, expiration, resolution, allow_short, max_pos)

        self._timer = timer

    def _fill_order(self, order: BaseOrder, price: Number) -> None:
        # calc changes in cash and contracts
        cash_delta = order.fill_cash_flow(price)
        fill_price = order.fill_price(price)
        contract_delta = order.fill_contract_flow()

        print(
            f"filled at (tte:{self.tte/3600}) (price: ${fill_price}) ", order)

        # apply changes
        self._cash += cash_delta
        self._position += contract_delta

    def _fill_all(self) -> None:
        # getting current data
        market = self.get_data()
        bid = market['bid']
        ask = market['ask']

        # orders not filled to be left as open
        orders_left = []

        # iterate through orders
        for order in self._orders:
            if (order.side == "buy") and (order.price >= ask):
                self._fill_order(order, ask)

            elif (order.side == "sell") and (order.price <= bid):
                self._fill_order(order, bid)

            else:
                orders_left.append(order)

        self._orders = orders_left

    def _resolve(self) -> None:
        """Resolve contracts if tte <=0
        """
        if self.tte <= 0:
            if self._resolution == 1:
                self._cash += self._position

            self._position = 0
            # print("contract resolved, cash bal:", self._cash)

    def start(self) -> None:
        self._data_feeder.start()

    def cycle(self) -> None:
        try:
            self._timer.cycle()
            self._fill_all()
        except SimFinished:
            # print("feed finished")
            pass
        self._resolve()

    def market_order(self, contracts: int, side: Literal["buy", "sell"]) -> None:
        self._orders.append(MarketOrder(count=contracts, side=side))

    def limit_order(self, contracts: int, side: Literal["buy", "sell"], price: Number) -> None:
        market = self.get_data()
        if (side == "buy") and (price >= market['ask']):
            self._orders.append(MarketOrder(count=contracts, side="buy"))
        elif (side == "sell") and (price <= market['bid']):
            self._orders.append(MarketOrder(count=contracts, side="sell"))
        else:
            self._orders.append(LimitOrder(
                count=contracts, side=side, price=price))

    def liquidate(self) -> None:
        contracts = -self._position
        side = "buy" if self.position < 0 else "sell"

        if contracts != 0:
            self._orders.append(MarketOrder(count=contracts, side=side))

    def clear_orders(self) -> None:
        self._orders = [
            order for order in self._orders if isinstance(order, MarketOrder)]

    def remove_orders(self, side=None, price=None) -> None:
        orders_left = [order for order in self._orders if ((order.side != side) and (
            order.price != price) and not isinstance(order, MarketOrder))]
        self._orders = orders_left
