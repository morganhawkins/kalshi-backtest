
from src.base import BaseModel
from . _utils import BinaryTree

# NOTE: noit sure hwo dag would work with path dependent terminal 
# values, so this would be a solution to this. painfully slow though
# TODO: estimate up/down factors from mu and sigma implied
# TODO: fill in value and greek exposure from _utils
class BTStepModel(BaseModel):

    def __init__(self, strike: int, expiration: float):
        super().__init__(strike, expiration)

        if not isinstance(strike, int):
            raise TypeError("`strike` must be an int for step contracts")
