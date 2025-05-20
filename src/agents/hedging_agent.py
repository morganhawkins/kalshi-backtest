from src.base import BaseDataFeeder
from src.base import BaseAgent
from src.base import BaseTimer
from src.models.geom_bm import GBMStepModel

class HedgingAgent(BaseAgent):
    def __init__(self, 
                 derivative_feeder: BaseDataFeeder, 
                 underlying_feeder: BaseDataFeeder, 
                 model: GBMStepModel, 
                 timer: BaseTimer
                 ):
        self.timer = timer
        self.deriv_feeder = derivative_feeder
        self.under_feeder = underlying_feeder
        self.model = model

        self.deriv_position = 0
        self.under_position = 0
        self.cash = 0

        self.last_deriv_price = None

        
    def valid_deriv_data(self, data: dict):
        # pickign arbitrary spread size
        if (data["ask"] - data['bid']) > .06:
            # if the spread is too big
            return False
        
        elif (data["ask"] > .97) or (data["bid"] < 0.03):
            # if ask or bid is too close ot the edge
            return False
        
        else:
            # if none of prev
            return True
            
    
    def consume(self):
        new_deriv_data = self.deriv_feeder.get()
        new_under_data = self.under_feeder.get()

        # if the new derivative data is valid ("there is a bid and an ask")
        if self.valid_deriv_data(new_deriv_data):
            price = (new_deriv_data["ask"] + new_deriv_data["bid"])/2
        else:
            price = self.last_deriv_price

        u_price = new_under_data["close"]
        estimated_sigma = new_under_data["24_hour_sigma_log"]
        estimated_mu = 0
        tte = new_deriv_data['tte']
        

        exposures = self.model(
            price=price,
            u_price=u_price,
            estimated_sigma=estimated_sigma,
            estimated_mu=estimated_mu,
            tte=tte)
        


    

    

