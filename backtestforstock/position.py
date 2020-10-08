import dataclasses
from datetime import datetime as dt
import pandas as pd
from logging import Logger
from backtestforstock.callbacks.core import PositionCallback

class PositionManager:
    def __init__(self,
                 logger: Logger,
                 is_allowed_short_position: bool=True):
        """
        :param is_allowed_short_position: Trueなら空売りを許す
        """
        self.logger = logger
        self.positions = []
        self.is_allowed_short_position = is_allowed_short_position
        self.id_max = 0

    def get_positions(self,
                      code: str) -> list:
        """
        指定した code のポジション一覧を返す
        :param code:
        :return: list
        """
        ret = []
        for position in self.positions:
            if position.code == code:
                ret.append(position)
        return ret

    def open_position(self,
                      code: str,
                      date: str,
                      amount: float,
                      price: float,
                      category: str):

        position = Position(id=self.id_max,
                            date=date,
                            code=code,
                            amount=amount,
                            price=price,
                            category=category)
        self.id_max += 1
        self.positions.append(position)
        return

    def close_position(self,
                       position,
                       amount: float):
        """
        ポジション position をクローズする
        :param position:
        :param amount:
        :return:
        """
        self.logger.debug(f"close前: {position}")
        position.amount -= amount
        self.logger.debug(f"close後: {position}")
        if position.amount == 0:
            self.positions.remove(position)
        return


@dataclasses.dataclass
class Position:
    id: int
    date: dt
    code: str
    category: str  # long or short
    amount: float  # if buy: plus; if sell: minus.
    price: float
    callback: list[PositionCallback] = []
