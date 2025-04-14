from abc import ABC, abstractmethod
from numbers import Number

class BaseTimer(ABC):
    """
    Base class for different Timers. Timers are used to track time. Can be 
        real time or can be accelerated to speed up simulation
    """

    @abstractmethod
    def cycle() -> None:
        """Method to cycle time
        """
        pass


    @abstractmethod
    def time() -> float:
        """Method to retrieve time

        Returns:
            (float): timestamp in seconds
        """
        pass