import pandas as pd
from logging import Logger
from backtestforstock.account import Account
from backtestforstock.position import Position, PositionManager
from .core import PositionCallback
from datetime import datetime as dt

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
                 logger: Logger = None,
                 limit_price: float = None,
                 stop_price: float = None):
        self.logger = logger
        self.limit_price = limit_price
        self.stop_price = stop_price

    def close(self,
              account: Account,
              date: dt,
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

        if limit_price is None or stop_price is None:
            amount = self.position.amount
        else:
            amount = self.position.amount / 2

        if limit_price is not None:
            account.close_position(position=self.position,
                                   amount=amount,
                                   price=limit_price,
                                   date=date)
        if stop_price is not None:
            account.close_position(position=self.position,
                                   amount=amount,
                                   price=stop_price,
                                   date=date)

    def on_step_begin(self,
                      account: Account,
                      data: pd.Series):
        """
        始値が指値、逆指値に引っかかっていたら取引
        約定値は始値
        :param account:
        :param data:
        :return:
        """

        if self.limit_price is None:
            limit_price = None
        elif data["open"] >= self.limit_price:
            limit_price = data["open"]
        else:
            limit_price = None

        if self.stop_price is None:
            stop_price = None
        elif data["open"] <= self.stop_price:
            stop_price = data["open"]
        else:
            stop_price = None

        self.close(account=account,
                   limit_price=limit_price,
                   stop_price=stop_price,
                   date=data["date"])


    def on_step_end(self,
                    account: Account,
                    data: pd.Series):
        """
        高値or安値が指値、逆指値に引っかかっていたら取引
        約定値はlimit_price/stop_priceの金額
        :param account:
        :param data:
        :return:
        """

        if self.limit_price is None:
            limit_price = None
        elif data["high"] >= self.limit_price:
            limit_price = self.limit_price
        else:
            limit_price = None

        if self.stop_price is None:
            stop_price = None
        elif data["low"] <= self.stop_price:
            stop_price = self.stop_price
        else:
            stop_price = None

        self.close(account=account,
                   limit_price=limit_price,
                   stop_price=stop_price,
                   date=data["date"])

    def __repr__(self):
        return f"OrderCallback(Logger={self.logger}, limit_price={self.limit_price}, stop_price={self.stop_price})"