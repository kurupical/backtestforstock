import pandas as pd
from backtestforstock.account import Account

class PositionCallback:

    def on_step_begin(self,
                      account: Account,
                      df: pd.DataFrame):
        pass

    def on_step_end(self,
                    account: Account,
                    df: pd.DataFrame):
        pass
