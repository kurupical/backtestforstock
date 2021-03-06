import pandas as pd
from datetime import datetime as dt
from .position import PositionManager, Position
from .history import HistoryManager, History
from backtestforstock.callbacks.core import PositionCallback
from logging import Logger
from typing import List

class Account:

    def __init__(self,
                 initial_cash: int,
                 logger: Logger
                 ):
        self.cash = initial_cash
        self.position_manager = PositionManager(logger=logger)
        self.history_manager = HistoryManager(logger=logger)
        self.logger = logger

    def _validate_order(self,
                        record: pd.Series,
                        amount: float,
                        price: float,
                        logger: Logger):
        """
        オーダー(buy, sell)が正しいことを確認
        :param df_data:
        :param code:
        :param amount:
        :param price:
        :param logger:
        :return:
        """
        if price >= record["high"]:
            raise ValueError(f"priceが当日高値より高いです。 price: {price}, data: {target_record}")

        if price <= record["low"]:
            raise ValueError(f"priceが当日安値より低いです。 price: {price}, data: {target_record}")

        return True

    def close_position(self,
                       position: Position,
                       amount: float,
                       price: float,
                       date: dt):
        self.position_manager.close_position(position=position,
                                             amount=amount)
        self.cash += amount * price
        if position.category == "short":
            category = "long"
        else:
            category = "short"

        self.history_manager.add(code=position.code,
                                 date=date,
                                 amount=amount,
                                 category=category,
                                 price=price,
                                 position=position)

    def open_position(self,
                      code: str,
                      date: dt,
                      amount: float,
                      price: float,
                      category: str,
                      callbacks: List[PositionCallback]):
        self.position_manager.open_position(code=code,
                                            date=date,
                                            amount=amount,
                                            price=price,
                                            category=category,
                                            callbacks=callbacks)
        self.history_manager.add(code=code,
                                 date=date,
                                 amount=amount,
                                 price=price,
                                 category=category)
        self.cash -= amount * price

    def trade(self,
              data: pd.Series,
              amount: float,
              price: float,
              category: str,
              callbacks: List[PositionCallback] = []):
        """
        data を price で amount だけ catergory に従って取引する
        反対ポジションを持ってる場合は相殺する
        :param data:
        :param amount:
        :param price:
        :param category: "long" or "short"
        :return:
        """
        self.logger.info(f"\n")
        self.logger.info(f"trade start! code: {data.code} amount: {amount}, price: {price}, category: {category}, cash: {self.cash}")
        category = category.lower()

        # callbacks(on_step_begin)
        positions = self.position_manager.get_positions(code=data["code"])
        for position in positions:
            for callback in position.callbacks:
                callback.on_step_begin(account=self,
                                       data=data)

        # close position
        positions = self.position_manager.get_positions(code=data["code"])
        for position in positions:
            if category == "long" and position.amount > 0:
                self.logger.debug("ignore: long and position.amount > 0")
                continue

            if category == "short" and position.amount < 0:
                self.logger.debug("ignore: short and position.amount < 0")
                continue

            if amount - position.amount >= 0:
                trade_amount = position.amount
            else:
                trade_amount = amount
            self.logger.debug(f"close position position: {position}, trade_amount: {trade_amount}")

            self.close_position(position=position,
                                amount=trade_amount,
                                price=price,
                                date=data.date)
            amount -= trade_amount

            if amount == 0:
                break

        # open position
        if self.cash < amount * price:
            self.logger.debug(f"所持金が不足しています。 cash: {self.cash}, buy: {amount * price}")
            return
        if amount < 0:
            raise ValueError("amountが負の値になってます。ライブラリのバグです。。 amount: {}".format(amount))
        if amount == 0:
            self.logger.debug(f"ポジション相殺のみで完了")
        if amount > 0:
            self.logger.debug(f"新規ポジション建て code: {data.code}, amount: {amount}, price: {price}")
            self.open_position(code=data.code,
                               date=data.date,
                               amount=amount,
                               price=price,
                               category=category,
                               callbacks=callbacks)

        # callbacks(on_step_end)
        positions = self.position_manager.get_positions(code=data["code"])
        for position in positions:
            for callback in position.callbacks:
                callback.on_step_end(account=self,
                                     data=data)

        self.logger.debug(f"trade end. cash: {self.cash}")


        return

    def report(self):
        pass

    def __del__(self):
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
