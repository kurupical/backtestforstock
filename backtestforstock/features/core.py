import pandas as pd
import copy

class FeatureProcessor:
    """
    生データから特徴量変換するプログラム
    """

    def __init__(self):
        pass

    def _transform_core(self, df):
        """
        特有部分
        :param df:
        :return:
        """
        raise NotImplementedError

    def transform(self,
                  df: pd.DataFrame):
        """

        :param df: 生データ
        :return: df: 加工された特徴量データ
        """

        return self._transform_core(copy.copy(df))
