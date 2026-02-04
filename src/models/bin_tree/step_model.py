
from src.base import BaseModel
from . _utils import BinaryTree


# TODO: estimate up/down factors from mu and sigma implied
# TODO: fill in value and greek exposure from _utils
class BTStepModel(BaseModel):

    def __init__(self, strike: int, expiration: float):
        super().__init__(strike, expiration)

        if not isinstance(strike, int):
            raise TypeError("`strike` must be an int for step contracts")
