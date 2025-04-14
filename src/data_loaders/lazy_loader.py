from pathlib import Path
from random import choice as random_choice
from typing import Optional, Generator, Tuple, Union
import os

import pandas as pd

from src.base import BaseDataLoader

class LazyLoader(BaseDataLoader):
    def __init__(self, root_dir: Path):
        if not os.path.isdir(root_dir): 
            raise ValueError(f"`root_dir` is not a directory {root_dir}")
        self._root_dir = root_dir

        self._map_dir()

    def _map_dir(self) -> None:
        dates = os.listdir(self._root_dir)
        dates = [dir_ for dir_ in dates if os.path.isdir(self._root_dir / dir_)]

        path_data = {}
        for date_ in dates:
            path_data[date_] = {}
            strike_fns = []
            for fn in os.listdir(self._root_dir / date_):
                strike = fn.split(".")[0]
                if ".csv" not in fn:
                    continue
                if not strike.isdigit():
                    continue

                path_data[date_][strike] = self._root_dir / date_ / fn

        self._path_data = path_data

    def query(self, date: str, strike: Union[int, str]) -> pd.DataFrame:
        path = self._path_data[date][str(strike)]
        data = pd.read_csv(path)

        return data
    
    def sample(self) -> pd.DataFrame:
        random_date = random_choice(list(self._path_data.keys()))
        random_strike = random_choice(list(self._path_data[random_date].keys()))

        return self.query(random_date, random_strike)

            
    def iterate(self, date: Optional[str]=None) -> Generator[Tuple[str, str, pd.DataFrame]]:
        """returns a generator to iterate over all points, or over a specific date of contracts 

        Args:
            date (Optional[str], optional): If specified will only iterate strikesin specified date. Otherwise, iterates over all dates

        Yields:
            Generator: generator to iterate over all date or, if specified, a specific date
        """
        if date is None:
            for date, strike_dict in self._path_data.items():
                for strike, path in strike_dict.items():
                    data = self.query(date, strike)
                    yield (date, strike, data)
        else:
            for strike, path in self._path_data[date].items():
                    data = self.query(date, strike)
                    yield (date, strike, data)
            