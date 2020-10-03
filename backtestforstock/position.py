import dataclasses
from datetime import datetime as dt

class PositionManager:
    def __init__(self,
                 is_allowed_short_position: bool=True):
        """
        :param is_allowed_short_position: Trueなら空売りを許す
        """
        self.positions = []
        self.is_allowed_short_position = is_allowed_short_position

    def buy(self):
        pass

    def sell(self):
        pass

@dataclasses.dataclass
class Position:
    id: int
    date: dt
    code: str
    amount: float  # if buy: plus; if sell: minus.
    price: float
