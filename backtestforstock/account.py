import pandas as pd
from datetime import datetime as dt
from .position import PositionManager, Position
from .hisotry import HistoryManager, History

class Account:

    def __init__(self,
                 initial_cash: int,
                 ):
        self.cash = initial_cash
        self.position_manager = PositionManager()
        self.history_manager = HistoryManager()

    def buy(self):
        pass

    def sell(self):
        pass

    def report(self):
        pass