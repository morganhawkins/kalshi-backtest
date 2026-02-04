import warnings

from tqdm import tqdm
import pandas as pd
import numpy as np

from src.exceptions import SimFinished
from src.agents import HedgingAgent
from src.backtester import FeederCreator

warnings.filterwarnings('ignore')


def get_terminal_port_values(max_under_pos: float, min_tte_hedge: float) -> list:
    """evaluate hedge strategy with the following two hyperparameters
    Args:
        max_under_pos (float): maximum magnitude of delta hedge in shares
        min_tte_hedge (float): will not rebalance hedge after this expiration time
    """
    end_values = []
    for deriv_feeder, under_feeder, timer, meta_data in FeederCreator.iterate(timedelta=60):

        # looping through contracts
        deriv_feeder.start()
        under_feeder.start()
        # init hedging agent
        agent = HedgingAgent(
            deriv_feeder, 
            under_feeder, 
            timer,
            meta_data['strike'], 
            max_under_pos=max_under_pos, 
            min_tte_hedge=min_tte_hedge
        )

        # cycle the timer & consume new data until simulation finished
        while True:
            timer.cycle()
            try:
                agent.consume()
            except SimFinished:
                # aggregate all trades performed and terminal deriv value
                terminal_u_price = meta_data['terminal_u_price']
                deriv_outcome = meta_data['outcome']
                net_end = agent.reconcile_hedge(terminal_u_price) + deriv_outcome
                end_values.append(net_end)
                break

    return end_values


if __name__ == "__main__":
    results = []

    # agent parameters
    max_max_under_pos = .0015
    max_min_tte_hedge = .7
    samples = 12

    # TODO: should probably use bayesian opt search, not exhaustive
    # grid search parameters
    for max_under_pos in (np.linspace(0, max_max_under_pos, samples)):
        for min_tte_hedge in tqdm(np.linspace(0, max_min_tte_hedge, samples)):
            # perform backtest
            end_values = get_terminal_port_values(
                max_under_pos=max_under_pos, 
                min_tte_hedge=min_tte_hedge
            )
            # agg results and append
            mean = np.mean(end_values)
            var = np.var(end_values)
            row = {
                "max_under_pos": max_under_pos,
                "min_tte_hedge": min_tte_hedge,
                "mean": mean,
                "var": var,
            }
            results.append(row)

    # save results
    res_df = pd.DataFrame(results)
    res_df.to_csv("hedge_agent_res.csv")

