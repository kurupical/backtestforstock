import unittest
from backtestforstock.strategies.core import Strategy
from backtestforstock.history import HistoryManager, History
from backtestforstock.position import PositionManager, Position
from backtestforstock.account import Account

from datetime import timedelta
from datetime import datetime as dt
import pandas as pd
import numpy as np

class BuyAnytimeStrategy(Strategy):
    """
    常に銘柄 code を amount だけ買う戦略(テスト用)
    """
    def __init__(self,
                 amount,
                 code="0000"):
        super().__init__()
        self.amount = amount

    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):
        account.buy(code=self.code, amount=self.amount)


class SellAnytimeStrategy(Strategy):
    """
    常にコード0000を amount だけ売る戦略
    """
    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):
        account.sell(code="0000", amount=self.amount)


class TestStrategies(unittest.TestCase):

    df_step1 = pd.DataFrame({"open": [100, 200],
                             "close": [200, 300],
                             "high": [250, 350],
                             "low": [50, 150],
                             "date": [dt(year=2020, month=1, day=1)+timedelta(days=x) for x in range(2)],
                             "code": ["0000"]*2})
    df_step2 = pd.DataFrame({"open": [100, 200, 300],
                             "close": [200, 300, 400],
                             "high": [250, 350, 450],
                             "low": [50, 150, 250],
                             "date": [dt(year=2020, month=1, day=1)+timedelta(days=x) for x in range(3)],
                             "code": ["0000"]*3})
    df_multi = pd.DataFrame({"open": [100, 200, 300, 400],
                             "close": [200, 300, 400, 500],
                             "high": [250, 350, 450, 550],
                             "low": [50, 150, 250, 350],
                             "date": [dt(year=2020, month=1, day=1)+timedelta(days=x) for x in range(2)]*2,
                             "code": ["0000"]*2 + ["1000"]*2})

    def test_buy_new(self):
        """
        新規購入(買い)
        :return:
        """
        account = Account(initial_cash=1_000_000)
        strategies = BuyAnytimeStrategy(code="0000", amount=100)

        strategies.trade(df_data=self.df_step1,
                         account=account)

        expect_positions = [
            Position(id=0,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=100,
                     price=200)
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=-100,
                    price_open=200,
                    price_close=np.nan)
        ]
        expect_cash = 1_000_000 - 200*100

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)



    def test_sell_new(self):
        """
        新規購入(売り)
        :return:
        """
        account = Account(initial_cash=1_000_000)
        strategies = SellAnytimeStrategy(code="0000", amount=100)

        strategies.trade(df_data=self.df_step1,
                         account=account)

        expect_positions = [
            Position(id=0,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=-100,
                     price=200)
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=-100,
                    price_open=200,
                    price_close=np.nan)
        ]

        expect_cash = 1_000_000 - 200*100

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)

    def test_buy_position_add(self):
        """
        同じコードを買い増し
        100株@200で購入, 100株@300で購入
        :return:
        """
        account = Account(initial_cash=1_000_000)
        strategies = BuyAnytimeStrategy(code="0000", amount=100)

        strategies.trade(df_data=self.df_step1,
                         account=account)
        strategies.trade(df_data=self.df_step2,
                         account=account)

        expect_positions = [
            Position(id=0,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=200,
                     price=100),
            Position(id=1,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=300,
                     price=100),
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=100,
                    price_open=200,
                    price_close=np.nan),
            History(id=1,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=100,
                    price_open=300,
                    price_close=np.nan)
        ]

        expect_cash = 1_000_000 - 200*100 - 300*100

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)

    def test_sell_position_close_all(self):
        """
        全部売却
        100株@200で購入, 100株@300で売却
        :return:
        """
        account = Account(initial_cash=1_000_000)

        # 買い
        strategies = BuyAnytimeStrategy(code="0000", amount=100)
        strategies.trade(df_data=self.df_step1,
                         account=account)

        strategies = SellAnytimeStrategy(code="0000", amount=100)
        strategies.trade(df_data=self.df_step2,
                         account=account)

        expect_positions = [
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=100,
                    price_open=200,
                    price_close=np.nan),
            History(id=1,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=-100,
                    price_open=200,
                    price_close=300)
        ]

        expect_cash = 1_000_000 + 100*100 # 100*100の利益

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)

    def test_sell_position_close_not_all(self):
        """
        一部売却
        100株@200で購入, 50株@300で売却
        :return:
        """
        account = Account(initial_cash=1_000_000)

        # 買い
        strategies = BuyAnytimeStrategy(code="0000", amount=100)
        strategies.trade(df_data=self.df_step1,
                         account=account)

        # 一部売却
        strategies = SellAnytimeStrategy(code="0000", amount=50)
        strategies.trade(df_data=self.df_step1,
                         account=account)

        expect_positions = [
            Position(id=0,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=50,
                     price=200),
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=100,
                    price_open=200,
                    price_close=np.nan),
            History(id=1,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=-50,
                    price_open=200,
                    price_close=300)
        ]

        expect_cash = 1_000_000 - 200*50 + 300*50

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)

    def test_sell_positions_close(self):
        """
        同一銘柄のポジションに絡む売却
        #1 code0000を100株@200で購入
        #2 code0000を200株@200で購入
        #3 code0000を200株@300で売却 -> #1 完全解消, #2 100解消
        :return:
        """
        account = Account(initial_cash=1_000_000)

        # 買い1
        strategies = BuyAnytimeStrategy(code="0000", amount=100)
        strategies.trade(df_data=self.df_step1,
                         account=account)

        # 買い2
        strategies = BuyAnytimeStrategy(code="0000", amount=200)
        strategies.trade(df_data=self.df_step1,
                         account=account)

        # 一部売却
        strategies = SellAnytimeStrategy(code="0000", amount=200)
        strategies.trade(df_data=self.df_step2,
                         account=account)

        expect_positions = [
            Position(id=1,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=100,
                     price=200),
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=100,
                    price_open=200,
                    price_close=np.nan),
            History(id=1,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=200,
                    price_open=200,
                    price_close=np.nan),
            History(id=2,  # Position #1
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=-100,
                    price_open=200,
                    price_close=300),
            History(id=3,  # Position #2
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=-100,
                    price_open=200,
                    price_close=300)
        ]

        expect_cash = 1_000_000 - 200*100 + 300*200

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)


    def test_sell_positions_close_multi_code(self):
        """
        別銘柄のポジションに絡む売却
        #1 code1000を100購入
        #2 code0000を200購入
        #3 code1000を200売却 -> #1 完全解消 + 空売り
        :return:
        """
        account = Account(initial_cash=1_000_000)

        # 買い1
        strategies = BuyAnytimeStrategy(code="1000", amount=100)
        strategies.trade(df_data=self.df_multi,
                         account=account)

        # 買い2
        strategies = BuyAnytimeStrategy(code="0000", amount=200)
        strategies.trade(df_data=self.df_multi,
                         account=account)

        # 一部売却
        strategies = SellAnytimeStrategy(code="1000", amount=200)
        strategies.trade(df_data=self.df_multi,
                         account=account)

        expect_positions = [
            Position(id=1,
                     date=self.base_dt["date"].iloc[-1],
                     code="0000",
                     amount=200,
                     price=200),
            Position(id=2,
                     date=self.base_dt["date"].iloc[-1],
                     code="1000",
                     amount=-100,
                     price=400),
        ]

        expect_histories = [
            History(id=0,
                    date=self.base_dt["date"].iloc[-1],
                    code="1000",
                    amount=100,
                    price_open=400,
                    price_close=np.nan),
            History(id=1,
                    date=self.base_dt["date"].iloc[-1],
                    code="0000",
                    amount=200,
                    price_open=200,
                    price_close=np.nan),
            History(id=2,
                    date=self.base_dt["date"].iloc[-1],
                    code="1000",
                    amount=-100,
                    price_open=400,
                    price_close=400),
            History(id=3,
                    date=self.base_dt["date"].iloc[-1],
                    code="1000",
                    amount=-100,
                    price_open=400,
                    price_close=np.nan),
        ]

        expect_cash = 1_000_000 - 400*100 - 200*200

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)

    def test_cash_shortage(self):
        """
        現金が足りない場合
        :return:
        """
        account = Account(initial_cash=100)
        strategies = BuyAnytimeStrategy(code="0000", amount=100)

        strategies.trade(df_data=self.df_step1,
                         account=account)

        expect_positions = [
        ]

        expect_histories = [
        ]

        expect_cash = 100

        self.assertEqual(expect_positions, account.position_manager.positions)
        self.assertEqual(expect_histories, account.history_manager.histories)
        self.assertEqual(expect_cash, account.cash)