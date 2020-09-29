import pandas as pd
from datetime import datetime as dt

class AccountInformation:

    def __init__(self,
                 initial_cash: int,
                 start_date: dt
                 ):
        self.cash = initial_cash
        self.start_date = start_date
        self.positions = pd.DataFrame()
        self.trading_histroy = pd.DataFrame()

    def get_positions(self):
        pass

    def append_history(self):
        pass