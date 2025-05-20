from pathlib import Path
from typing import Generator, Literal, Dict, List, Tuple

import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt

from src.data_feeder.sim_data_feeder import SimDataFeeder
from src.timers import DeltaTimer
from src.data_loaders import LazyLoader

class FeederCreator:
    """helper class to create appropriate data feeders from a date and strike"""

    def __init__(self):
        pass
    
    @staticmethod
    def make_feeder_feeder(data: pd.DataFrame) -> Dict[Literal["time", "value"], List]:
        time = data['ts'].tolist()
        value = [dict(row) for i, row in data.iterrows()]

        return {"time": time, "value": value}
        
    @classmethod
    def iterate(cls,
                deriv_data_path: str="/Users/morganhawkins/Projects/stale/Kalshi_Stale/data/btc_data/step",
                under_data_path: str="/Users/morganhawkins/Projects/stale/Kalshi_Stale/data/btc_underlying.csv",
                timedelta: int=60
                ) -> Generator[Tuple[SimDataFeeder, SimDataFeeder, DeltaTimer, Dict]]:
        loader = LazyLoader(Path(deriv_data_path))
        under_data = pd.read_csv(under_data_path)

        for date, strike, data in loader.iterate():
            #  auto-skip short data
            if len(data) < 5: continue

            #  grabbing relevant underlying data
            hist_start = data["ts"].min()
            expiration_ts = data["ts"][0] + (data["tte"][0]*3600)
            active_u_data = under_data[(under_data["ts"] <= expiration_ts + 600) & (under_data['ts'] >= hist_start)]

            # making timer to link feeders
            timer = DeltaTimer(timedelta)

            # underlying feeder
            u_hist_dict = cls.make_feeder_feeder(active_u_data)
            under_feeder = SimDataFeeder(hist_start, expiration_ts, u_hist_dict, timer)

            # deriv feeder
            d_hist_dict = cls.make_feeder_feeder(data)
            deriv_feeder = SimDataFeeder(hist_start, expiration_ts, d_hist_dict, timer)

            # compiling metadata
            outcome = active_u_data[active_u_data["ts"] <= expiration_ts]["close"].tolist()[-1]
            outcome = outcome >= int(strike)

            meta_data = {"strike": strike,
                         "date": date,
                         "outcome": outcome,
                         "data_points": len(data),
                         "expiration_ts": expiration_ts}

            yield deriv_feeder, under_feeder, timer, meta_data


    @classmethod
    def iterate_plots(cls,
                      deriv_data_path: str="/Users/morganhawkins/Projects/stale/Kalshi_Stale/data/btc_data/step",
                      under_data_path: str="/Users/morganhawkins/Projects/stale/Kalshi_Stale/data/btc_underlying.csv",
                      ) -> Generator:
        print(deriv_data_path)
        loader = LazyLoader(Path(deriv_data_path))
        under_data = pd.read_csv(under_data_path)

        for date, strike, data in loader.iterate():
            #  auto-skip short data
            if len(data) < 1000: continue

            #  grabbing relevant underlying data
            hist_start = data["ts"].min()
            expiration_ts = data["ts"][0] + (data["tte"][0]*3600)
            active_u_data = under_data[(under_data["ts"] <= expiration_ts + 600) & (under_data['ts'] >= hist_start)]

            plt.figure(figsize=(15,5))

            plt.subplot(1,2,1)
            plt.title("Underlying")
            plt.plot([dt.datetime.fromtimestamp(ts) for ts in active_u_data.ts], active_u_data.close)
            plt.axhline(y=int(strike), label="strike", color="red")
            plt.xlabel("mm-dd H")
            plt.legend()
            plt.xticks(rotation=45)

            plt.subplot(1,2,2)
            plt.title("Derivative")
            plt.ylim(0,1)
            plt.scatter([dt.datetime.fromtimestamp(ts) for ts in data['ts']], data["bid"]/100, s=1)
            plt.xticks(rotation=45)

            plt.xlabel("mm-dd H")
            plt.show()

            yield

        
