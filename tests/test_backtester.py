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

class CustomStrategy(Strategy):
    """
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
    def test_normal(self):
        """
        全銘柄、毎日100株ずつ買い、200株になったら売る
        :return:
        """
        data_fetcher = DataFetcher(df=pd.concat([self.df_0000, self.df_1000]),
                                   start_datetime=dt(year=2020, month=1, day=1))
        strategy = CustomStrategy()
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


if __name__ == "__main__":
    unittest.main()