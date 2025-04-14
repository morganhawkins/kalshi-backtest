from abc import ABC, abstractmethod
from typing import Optional, Generator
from pathlib import Path

class BaseDataLoader(ABC):

    def __init__(self, root_dir: Path):
        self._root_dir = root_dir

    @abstractmethod
    def iterate(self, date: Optional[str]=None) -> Generator:
        """returns a generator to iterate over all points, or over a specific date of contracts 

        Args:
            date (Optional[str], optional): If specified will only iterate strikesin specified date. Otherwise, iterates over all dates

        Yields:
            Generator: generator to iterate over all date or, if specified, a specific date
        """
        pass