from abc import ABC, abstractmethod

class BaseTimer(ABC):
    """
    Base class for different Timers. Timers are used to track time. Can be 
        real time or can be accelerated to speed up simulation
    """

    @abstractmethod
    def time() -> float:
        """
        Method to retrieve time

        Returns:
            (float): timestamp in seconds
        """
        pass