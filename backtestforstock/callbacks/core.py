import pandas as pd
from logging import Logger
# from backtestforstock.account import Account
# from backtestforstock.position import Position


class PositionCallback:
    """
    def on_step_begin(self,
                      account: Account,
                      df: pd.DataFrame):
        raise NotImplementedError

    def on_step_end(self,
                    account: Account,
                    df: pd.DataFrame):
        raise NotImplementedError
    """
    def set_position(self,
                     position):
        self.position = position

    def set_logger(self,
                   logger: Logger):
        self.logger = logger