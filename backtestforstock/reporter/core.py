from backtestforstock.account import Account
import dataclasses


class Reporter:
    def __init__(self, **kwargs):
        pass

    def output_report(self,
                      account: Account):
        raise NotImplementedError


@dataclasses.dataclass
class ProfitAndLossSummary:
    """
    pl_amount: profit/loss/earn money amount
    pl_mean: 取引回数あたりのpl_amount平均
    trade_amount: 取引金額合計
    trade_count: 取引回数
    """
    pl_amount: float
    pl_mean: float
    trade_amount: float
    trade_count: int


@dataclasses.dataclass
class Summary:
    earn_summary: ProfitAndLossSummary
    profit_summary: ProfitAndLossSummary
    loss_summary: ProfitAndLossSummary

