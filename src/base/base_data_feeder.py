from abc import ABC, abstractmethod
from typing import Any

class BaseDataFeeder(ABC):
    @abstractmethod
    def get(self) -> Any:
        """
        Returns:
            (Any): Relevant data
        """
        pass
    
