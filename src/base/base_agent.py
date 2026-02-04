from typing import Dict
from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @abstractmethod
    def consume(self):
        pass
