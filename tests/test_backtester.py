import unittest
import pandas as pd
import numpy as np
from backtestforstock.backtester import convert_date_step_interval
from backtestforstock.strategies.core import Strategy
from backtestforstock.account import Account
from backtestforstock.datafetchers.core import DataFetcher
from backtestforstock.features.empty import NothingProcessor
from backtestforstock.backtester import BackTester
from backtestforstock.common import get_logger
from backtestforstock.callbacks.order import OrderCallback
from datetime import timedelta
from datetime import datetime as dt

class TestValidateDateStepInterval(unittest.TestCase):
    def test_1m(self):
        expect = timedelta(minutes=1)
        actual = convert_date_step_interval("1m")
        self.assertEqual(expect, actual)

    def test_1h(self):
        expect = timedelta(hours=1)
        actual = convert_date_step_interval("1h")
        self.assertEqual(expect, actual)

    def test_1d(self):
        expect = timedelta(days=1)
        actual = convert_date_step_interval("1d")
        self.assertEqual(expect, actual)

    def test_error_format(self):
        with self.assertRaises(ValueError):
            convert_date_step_interval("10y")

    def test_error_format2(self):
        with self.assertRaises(ValueError):
            convert_date_step_interval("1yy")


class BuyAndSellStrategy(Strategy):
    """
    test_normal 用のクラス
    毎日100株ずつ買い、200株になったら売る
    """

    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):

        for code, df in df_data.groupby("code"):
            positions = account.position_manager.get_positions(code)
            total_amount = 0
            for position in positions:
                total_amount += position.amount

            if total_amount < 200:
                account.trade(data=df.iloc[-1],
                              amount=100,
                              price=df.iloc[-1]["open"],
                              category="long")
            else:
                account.trade(data=df.iloc[-1],
                              amount=200,
                              price=df.iloc[-1]["open"],
                              category="short")

class LimitTwiceStrategy(Strategy):
    """
    test_hit_limit_order 用のクラス
    全銘柄、指値を購入株価の倍にする
    """

    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):

        for code, df in df_data.groupby("code"):
            positions = account.position_manager.get_positions(code)
            total_amount = 0
            for position in positions:
                total_amount += position.amount

            price = df.iloc[-1]["open"]
            if total_amount < 200:
                account.trade(data=df.iloc[-1],
                              amount=100,
                              price=price,
                              category="long",
                              callbacks=[OrderCallback(limit_price=price*2)]
                              )
            else:
                account.trade(data=df.iloc[-1],
                              amount=200,
                              price=price,
                              category="short",
                              callbacks=[OrderCallback(limit_price=price*2))


class StopHalfStrategy(Strategy):
    """
    test_hit_stop_order 用のクラス
    全銘柄、逆指値を購入株価の半分にする
    """

    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):

        for code, df in df_data.groupby("code"):
            positions = account.position_manager.get_positions(code)
            total_amount = 0
            for position in positions:
                total_amount += position.amount

            price = df.iloc[-1]["open"]
            if total_amount < 200:
                account.trade(data=df.iloc[-1],
                              amount=100,
                              price=price,
                              category="long",
                              callbacks=[OrderCallback(stop_price=price/2)]
                              )
            else:
                account.trade(data=df.iloc[-1],
                              amount=200,
                              price=price,
                              category="short",
                              callbacks=[OrderCallback(stop_price=price*2))


class LimitTwiceAndStopHalfStrategy(Strategy):
    """
    test_hit_limit_stop_order 用のクラス
    全銘柄、逆指値を購入株価の半分にする
    """

    def _trade_core(self,
                    df_data: pd.DataFrame,
                    account: Account):

        for code, df in df_data.groupby("code"):
            positions = account.position_manager.get_positions(code)
            total_amount = 0
            for position in positions:
                total_amount += position.amount

            price = df.iloc[-1]["open"]
            if total_amount < 200:
                account.trade(data=df.iloc[-1],
                              amount=100,
                              price=price,
                              category="long",
                              callbacks=[OrderCallback(limit_price=price*2, stop_price=price/2)]
                              )
            else:
                account.trade(data=df.iloc[-1],
                              amount=200,
                              price=price,
                              category="short",
                              callbacks=[OrderCallback(limit_price=price*2, stop_price=price*2))

class TestBackTester(unittest.TestCase):
    df_0000 = pd.DataFrame({"open": [100, 200, 300, 400, 500],
                            "close": [200, 300, 400, 500, 600],
                            "high": [250, 350, 450, 550, 650],
                            "low": [50, 150, 250, 350, 450],
                            "date": [dt(year=2020, month=1, day=1)+timedelta(days=x) for x in range(5)],
                            "code": ["0000"]*5})
    df_1000 = pd.DataFrame({"open": [200, 400, 600, 800, 1000],
                            "close": [300, 500, 700, 900, 1100],
                            "high": [350, 550, 750, 950, 1150],
                            "low": [150, 350, 550, 750, 950],
                            "date": [dt(year=2020, month=1, day=1)+timedelta(days=x) for x in range(5)],
                            "code": ["1000"]*5})
    df_2000 = pd.DataFrame({"open": [200, 120, 80, 60, 40],
                            "close": [120, 80, 70, 40, 35],
                            "high": [200, 140, 160, 60, 120],
                            "low": [100, 80, 70, 40, 30],
                            "date": [dt(year=2020, month=1, day=1)+timedelta(days=x) for x in range(5)],
                            "code": ["2000"]*5})

    def test_normal(self):
        """
        全銘柄、毎日100株ずつ買い、200株になったら売る
        :return:
        """
        data_fetcher = DataFetcher(df=pd.concat([self.df_0000, self.df_1000]),
                                   start_datetime=dt(year=2020, month=1, day=1))
        strategy = BuyAndSellStrategy()
        account = Account(initial_cash=1_000_000,
                          logger=get_logger())

        backtester = BackTester(data_fetcher=data_fetcher,
                                strategy=strategy,
                                account=account,
                                date_step_interval="1d")

        backtester.run()

        expect_cash = 1_000_000
        expect_cash -= 100*100 + 200*100   # 1日目
        expect_cash -= 200*100 + 400*100   # 2日目
        expect_cash += 300*200 + 600*200   # 3日目
        expect_cash -= 400*100 + 800*100   # 4日目
        expect_cash -= 500*100 + 1000*100  # 5日目

        self.assertEqual(expect_cash, backtester.account.cash)

    def test_hit_limit_order(self):
        """
        全銘柄、指値を購入株価の倍にする
        :return:
        """
        data_fetcher = DataFetcher(df=pd.concat([self.df_0000, self.df_1000]),
                                   start_datetime=dt(year=2020, month=1, day=1))
        strategy = LimitTwiceStrategy()
        account = Account(initial_cash=1_000_000,
                          logger=get_logger())

        backtester = BackTester(data_fetcher=data_fetcher,
                                strategy=strategy,
                                account=account,
                                date_step_interval="1d")
        backtester.run()

        expect_cash = 1_000_000
        # code=0000
        expect_cash -= 100*100   # 1日目
        expect_cash += 200*100   # 1日目(指値hit on_batch_end 100->200)
        expect_cash -= 200*100   # 2日目
        expect_cash -= 300*100   # 3日目
        expect_cash += 400*100   # 3日目(指値hit on_batch_end 200->400)
        expect_cash -= 400*100   # 4日目
        expect_cash -= 500*100   # 5日目
        expect_cash += 600*100   # 5日目(指値hit on_batch_end 300->600)

        # code=1000
        expect_cash -= 200*100   # 1日目
        expect_cash += 400*100   # 2日目(指値hit on_batch_start 200->400)
        expect_cash -= 400*100   # 2日目
        expect_cash -= 600*100   # 3日目
        expect_cash += 800*100   # 4日目(指値hit on_batch_start 400->800)
        expect_cash -= 800*100   # 4日目
        expect_cash -= 1000*100  # 5日目

        self.assertEqual(expect_cash, backtester.account.cash)

    def test_hit_stop_order(self):
        """
        全銘柄、逆指値を購入株価の半分にする
        :return:
        """
        data_fetcher = DataFetcher(df=self.df_2000,
                                   start_datetime=dt(year=2020, month=1, day=1))
        strategy = StopHalfStrategy()
        account = Account(initial_cash=1_000_000,
                          logger=get_logger())

        backtester = BackTester(data_fetcher=data_fetcher,
                                strategy=strategy,
                                account=account,
                                date_step_interval="1d")
        backtester.run()

        expect_cash = 1_000_000
        # code=2000
        expect_cash -= 200*100  # 1日目
        expect_cash += 100*100  # 1日目_hit
        expect_cash -= 120*100  # 2日目
        expect_cash -= 80*100   # 3日目
        expect_cash += 60*100   # 4日目_hit
        expect_cash -= 60*100   # 4日目
        expect_cash += 40*100   # 4日目_hit
        expect_cash -= 40*100   # 5日目
        expect_cash += 30*100   # 5日目_hit

        self.assertEqual(expect_cash, backtester.account.cash)

    def test_hit_limit_stop_order(self):
        """
        全銘柄、逆指値を購入株価の半分にする
        (指値・逆指値両方同時にあたったら、ポジションを半分ずつにする)
        :return:
        """
        data_fetcher = DataFetcher(df=self.df_2000,
                                   start_datetime=dt(year=2020, month=1, day=1))
        strategy = LimitTwiceAndStopHalfStrategy()
        account = Account(initial_cash=1_000_000,
                          logger=get_logger())

        backtester = BackTester(data_fetcher=data_fetcher,
                                strategy=strategy,
                                account=account,
                                date_step_interval="1d")
        backtester.run()

        expect_cash = 1_000_000
        # code=2000
        expect_cash -= 200*100  # 1日目
        expect_cash += 100*100  # 1日目_hit(stop 200)
        expect_cash -= 120*100  # 2日目
        expect_cash -= 80*100   # 3日目
        expect_cash += 160*100  # 3日目_hit(limit 80)
        expect_cash += 60*100   # 4日目_hit(stop 120)
        expect_cash -= 60*100   # 4日目
        expect_cash -= 40*100   # 5日目
        expect_cash += 80*100   # 5日目_hit(limit 40 high=120だけど80で刺さってること)
        expect_cash += 120*50   # 5日目_hit(limit 60 limit&stop同時刺さり)
        expect_cash += 30*50    # 5日目_hit(stop 60 limit&stop同時刺さり)

        self.assertEqual(expect_cash, backtester.account.cash)




if __name__ == "__main__":
    unittest.main()