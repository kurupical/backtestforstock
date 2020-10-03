from .core import FeatureProcessor
import pandas as pd

class NothingProcessor(FeatureProcessor):
    """
    何も特徴量変換しない
    """

    def transform(self,
                  df: pd.DataFrame):
        """

        :param df: 生データ
        :return: df: 加工された特徴量データ
        """

        return df