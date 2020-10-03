
from backtestforstock.datafetchers.core import DataFetcher
from backtestforstock.features.core import FeatureProcessor
from backtestforstock.strategies.core import Strategy
from backtestforstock.account import Account
from datetime import timedelta


def validate_date_step_interval(s: str) -> timedelta:
    if s[-1] not in ["m", "h", "d"]:
        raise ValueError(f"date_step_interval の単位は m, h, dのみ使用可能です。 入力: {s}")

    interval_num = float(s[:-1])
    if s[-1] == "m":
        return timedelta(minutes=interval_num)
    if s[-1] == "h":
        return timedelta(hours=interval_num)
    if s[-1] == "d":
        return timedelta(days=interval_num)


class Backtester:

    def __init__(self,
                 data_fetcher: DataFetcher,
                 feature_processor: FeatureProcessor,
                 strategy: Strategy,
                 account_info: Account,
                 date_step_interval: str
                 ):
        """

        :param data_fetcher:
        :param feature_processor:
        :param strategy:
        :param account_info:
        :param date_step_interval: "m", "h", "d" can use example: "10m", "1h", "2d"
        """
        self.data_fetcher = data_fetcher
        self.feature_processor = feature_processor
        self.strategy = strategy
        self.account_info = account_info
        self.date_step_interval = date_step_interval


    def backtest(self):
        while True:
            self.step()

    def step(self):
        df_data = self.data_fetcher.fetch_data()
        df_processed = self.feature_processor.transform(df=df_data)
        self.account_info = self.strategy.trade(df_processed, self.account_info)
