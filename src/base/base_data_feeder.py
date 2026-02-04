from abc import ABC, abstractmethod
from typing import Any


class BaseDataFeeder(ABC):
    @abstractmethod
    def time(self) -> float:
        """Time that the datafeeder is basing its data off

        Returns:
            float: unix timestamp of feeders time
        """
        pass

    @abstractmethod
    def get(self) -> Any:
        """
        Returns:
            (Any): Relevant data
        """
        pass
