import dataclasses
from datetime import datetime as dt

class HistoryManager:
    def __init__(self):
        self.histories = []

    def add(self):
        pass


@dataclasses.dataclass
class History:
    id: int
    date: dt
    code: str
    amount: float  # if buy: plus; if sell: minus.
    price_open: float
    price_close: float
