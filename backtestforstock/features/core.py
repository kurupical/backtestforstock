import pandas as pd
import copy

class FeatureProcessor:
    """
    生データから特徴量変換するプログラム
    """

    def __init__(self, **kwargs):
        pass

    def _transform_core(self, df):
        """
        特有部分
        :param df:
        :return:
        """
        raise NotImplementedError

    def _validate(self,
                  df_original: pd.DataFrame,
                  df_transform: pd.DataFrame):

        expect_same_cols = ["date", "code", "open", "close", "high", "low", "volume"]

        pd.testing.assert_frame_equal(df_original[expect_same_cols],
                                      df_transform[expect_same_cols])

    def transform(self,
                  df: pd.DataFrame):
        """

        :param df: 生データ
        :return: df: 加工された特徴量データ
        """

        df_ret = self._transform_core(copy.copy(df))
        self._validate(df_original=df,
                       df_transform=df_ret)

        return df_ret