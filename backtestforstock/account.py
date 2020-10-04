import pandas as pd
from datetime import datetime as dt
from .position import PositionManager, Position
from .history import HistoryManager, History
from logging import Logger

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

    def trade(self,
              data: pd.Series,
              amount: float,
              price: float,
              category: str):
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
        # close position
        positions = self.position_manager.get_positions(code=data["code"])

        category = category.lower()
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

            self.position_manager.close_position(position=position,
                                                 amount=trade_amount)
            amount -= trade_amount
            self.cash += trade_amount * price

            self.history_manager.add(data=data,
                                     amount=trade_amount,
                                     category=category,
                                     price=price,
                                     position=position)
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
            self.position_manager.open_position(data=data,
                                                amount=amount,
                                                price=price,
                                                category=category)
            self.history_manager.add(data=data,
                                     amount=amount,
                                     price=price,
                                     category=category)
            self.cash -= amount * price

        self.logger.debug(f"trade end. cash: {self.cash}")
        return

    def report(self):
        pass

    def __del__(self):
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
