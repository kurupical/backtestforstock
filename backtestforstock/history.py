import dataclasses
import numpy as np
import pandas as pd
from datetime import datetime as dt
from .position import Position
from logging import Logger

class HistoryManager:
    def __init__(self,
                 logger: Logger):
        self.histories = []
        self.logger = logger
        self.id_max = 0

    def add(self,
            code: str,
            date: dt,
            amount: float,
            price: float,
            category: str,
            position=None):
        if position == None:
            history = History(id=self.id_max,
                              code=code,
                              date=date,
                              amount=amount,
                              category=category,
                              price_open=price,
                              price_close=np.nan)
        else:
            history = History(id=self.id_max,
                              code=code,
                              date=date,
                              amount=amount,
                              category=category,
                              price_open=position.price,
                              price_close=price,
                              id_close=position.id)
        self.histories.append(history)
        self.id_max += 1
        return

@dataclasses.dataclass
class History:
    id: int
    date: dt
    code: str
    category: str  # long or short
    amount: float  # if buy: plus; if sell: minus.
    price_open: float
    price_close: float = None
    id_close: int = None
