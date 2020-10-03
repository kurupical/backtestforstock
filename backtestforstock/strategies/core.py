import pandas as pd
from backtestforstock.account import Account

class Strategy:
    """
    取引アルゴリズム
    """

    def __init__(self, **kwargs):
        pass

    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):
        raise NotImplementedError

    def trade(self,
              df_data: pd.DataFrame,
              account: Account):
        self._trade_core(df_data=df_data,
                         account=account)

    def buy(self,
            code: str,
            amount: float):
        pass # TODO: implement

    def sell(self):
        pass # TODO: implement
