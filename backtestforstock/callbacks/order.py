import pandas as pd
from backtestforstock.account import Account
from backtestforstock.position import Position, PositionManager
from .core import PositionCallback

class OrderCallback(PositionCallback):
    """
    指値/逆指値コールバック。
    取引前・取引後に指値、逆指値を確認する

    Attributes
    ----------
    limit_price: float, default: None
        指値金額。defaultは指値無し

    stop_price: float, default: None
        逆指値金額。dafaultは指定無し。
    """

    def __init__(self,
                 position: Position,
                 limit_price: float = None,
                 stop_price: float = None):
        self.position = position
        self.limit_price = limit_price
        self.stop_price = stop_price

    def close(self,
              account: Account,
              position_manager: PositionManager,
              limit_price: float=None,
              stop_price: float=None):
        """
        ポジションをクローズする
        :param account:
        :param position_manager:
        :param limit_price:
        :param stop_price:
        :return:
        """
        account.close_position(position=self.position)



    def on_step_begin(self,
                      account: Account,
                      df: pd.DataFrame):
        """
        始値が指値、逆指値に引っかかっていたら取引(その金額で)
        :param account:
        :param df:
        :return:
        """
        series = df[df["code"] == self.position.code].iloc[-1]

        if series["open"] >= self.limit_price:
            limit_price = series["open"]
        else:
            limit_price = None

        if series["open"] <= self.stop_price:
            stop_price = series["open"]
        else:
            stop_price = None

        self.close(position_manager=account.position_manager,
                   limit_price=limit_price,
                   stop_price=stop_price)
