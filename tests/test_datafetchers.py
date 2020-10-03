import unittest
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from backtestforstock.datafetchers.core import DataFetcher

class TestDataFetchers(unittest.TestCase):
    def test_fetch(self):
        base_dt = dt(year=2020, month=1, day=1)
        df = pd.DataFrame({"open": [0, 1, 2, 3, 4],
                           "close": [1, 2, 3, 4, 5],
                           "high": [2, 3, 4, 5, 6],
                           "low": [0, 1, 2, 3, 4],
                           "date": [base_dt+timedelta(days=x) for x in range(5)],
                           "code": ["test"]*5})

        datafetcher = DataFetcher(df=df,
                                  start_datetime=base_dt)

        df_expect = df.iloc[:2]
        df_actual = datafetcher.fetch(step=timedelta(days=1))

        pd.testing.assert_frame_equal(df_expect, df_actual)

if __name__ == "__main__":
    unittest.main()