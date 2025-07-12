from numpy import isnan
from numpy import round as np_round

from src.base import BaseDataFeeder
from src.base import BaseAgent
from src.base import BaseTimer
from src.models.geom_bm import GBMStepModel

class UnderlyingOrder:
    def __init__(self,exec_price: float, quantity: float):
        self.exec_price = exec_price
        self.quantity = quantity
        
    def accum(self, curr_price) -> float:
        return self.quantity * (curr_price - self.exec_price)

class HedgingAgent(BaseAgent):
    def __init__(self, 
                 derivative_feeder: BaseDataFeeder, 
                 underlying_feeder: BaseDataFeeder, 
                 timer: BaseTimer,
                 strike: float,
                 max_under_pos: float=.0005,
                 min_tte_hedge: float=.15
                 ):
        self.timer = timer
        self.deriv_feeder = derivative_feeder
        self.under_feeder = underlying_feeder
        self.model = GBMStepModel
        self.strike = strike

        # tracking positions
        self.under_orders = [] 
        self.under_position = 0 # in num shares
        self.deriv_position = 0 # in num contracts
        self.cash = 0 # in dollars

        # hedging position restraints
        self.max_under_pos = max_under_pos
        self.min_tte_hedge = min_tte_hedge

        # track terminal underlying value
        self.underlying_terminal_value = None
 
        
    def valid_deriv_data(self, data: dict) -> bool:
        # pickign arbitrary spread size
        if (data["ask"] - data['bid']) > 5:
            # if the spread is too big
            # print("spread too big")
            return False
        
        elif (data["ask"] > 95) or (data["bid"] < 5):
            # if ask or bid is too close ot the edge
            return False
        
        else:
            # if none of prev
            return True
        
    def close_to_expiration(self, data: dict) -> bool:
        if data['tte'] < self.min_tte_hedge:
            #too close to expiration to hedge
            return True
        
        return False
    
    def purchase_deriv(self, data: dict) -> None:
        if self.deriv_position == 0:
            # assume execution at mid-market price
            execution_price = (data['ask'] - data['bid'])/200
            
            # updating portfolio
            self.deriv_position += 1
            self.cash -= execution_price

    def purchase_underlying(self, data: dict, quantity: float) -> None:
        if quantity > 0:
            quantity = max(min(self.max_under_pos - self.under_position, quantity), 0)
        else:
            quantity = min(max(-self.max_under_pos - self.under_position, quantity), 0)

        if quantity != 0:
            order = UnderlyingOrder(exec_price=data['open'], quantity=quantity)
            self.under_orders.append(order)
            self.under_position += quantity

    def portfolio_delta(self, exposures: dict) -> float:
        deriv_delta_exposure = exposures['delta']
        portfolio_delta = (self.deriv_position * deriv_delta_exposure) + self.under_position
        return portfolio_delta

    def rebalance_hedge(self, u_data: dict, exposures: dict) -> None:
        portfolio_delta = self.portfolio_delta(exposures)
        self.purchase_underlying(u_data, -portfolio_delta)

    def zero_hedge(self, u_data: dict) -> None:
        self.purchase_underlying(u_data, -self.under_position)

    def reconcile_hedge(self, u_price):
        return sum(order.accum(u_price) for order in self.under_orders)

    def consume(self):
        new_deriv_data = self.deriv_feeder.get()
        new_under_data = self.under_feeder.get()
        
        d_price = (new_deriv_data["ask"] + new_deriv_data["bid"])/200
        u_price = new_under_data["open"]
        estimated_sigma = new_under_data["4_hour_sigma_log"]
        tte = new_deriv_data['tte']

        # exposures use iv for volatility estimate
        exposures = self.model.__call__(
            price=d_price,
            u_price=u_price,
            estimated_sigma=estimated_sigma,
            estimated_mu=0,
            tte=tte,
            strike=self.strike)
        exposures['portfolio_delta'] = self.portfolio_delta(exposures)

        
        #if close to expiration, zero the hedge and carry the contract to expiration
        if self.close_to_expiration(new_deriv_data):
            if self.under_position != 0:
                self.zero_hedge(new_under_data)

        elif self.valid_deriv_data(new_deriv_data):
            # purchasing a derivative contract if it's not already purchased 
            self.purchase_deriv(new_deriv_data)

            # rebalancing elta hedge
            self.rebalance_hedge(new_under_data, exposures)

            

        return exposures


        exposures_rounded = {k:np_round(v,4) for k,v in exposures.items()}
        # if isnan(exposures['iv']):
        print("-"*100)
        print("            tte:", tte)
        print("     port_delta:", exposures['portfolio_delta'])
        print(" hedge_quantity:", self.under_position)
        print("       in money:", self.strike < u_price)
        print("            bid:", new_deriv_data["bid"])
        print("            ask:", new_deriv_data["ask"])
        print("     price_used:", round(d_price, 2))
        print("(strike, price):", f"({self.strike}, {u_price})")
        print("      est sigma:", estimated_sigma)
        print("      imp sigma:", exposures_rounded['iv'])
        print("          expos:", exposures_rounded)

        return exposures

        

        


    

    

