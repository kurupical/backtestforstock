import pandas as pd
from glob import glob
from datetime import timedelta
from datetime import datetime as dt

class DataFetcher:
    """
    株価等のデータをフェッチするクラス

    """
    def __init__(self,
                 data_files: list = None,
                 df: pd.DataFrame = None,
                 start_datetime: dt = None):
        """
        DataFetcherにDataFrameをセットする
        セットの方法は2通り。data_filesにファイルをセットするか、dfに直接DataFrameをセットする
        :param data_dir:
        :param df:
        """
        self.data_files = data_files

        if data_files is not None:
            self.df_data = pd.concat([pd.read_csv(x) for x in self.data_files])
        elif df is not None:
            self.df_data = df
        else:
            raise AttributeError("data_filesとdfが両方Nullです")
        self._validate_data(self.df_data)
        self.datetime = start_datetime

    def _validate_data(self, df):
        should_existing_columns = ["open", "close", "high", "low", "date", "code"]

        for col in should_existing_columns:
            if col not in df:
                raise ValueError(
                    f"""
                    DataFetcherに入力するデータは、カラム{should_existing_columns}が必要ですが
                    カラム{col}が入力データに存在しません。データを確認してください。
                    """
                )

    def fetch(self, step=timedelta):
        self.datetime += step
        df_fetch = self.df_data[self.df_data["date"] <= self.datetime]
        return df_fetch