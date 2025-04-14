
from src.base import BaseModel
from . _utils import DAG


# TODO: estimate up/down from mu and sigma implied
class DAGStepModel(BaseModel):

    def __init__(self, strike: int, expiration: float):
        super().__init__(strike, expiration)

        if not isinstance(strike, int):
            raise TypeError("`strike` must be an int for step contracts")
        