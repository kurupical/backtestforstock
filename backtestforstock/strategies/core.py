

class Strategy:
    """
    取引アルゴリズム
    """

    def __init__(self):
        pass

    def _trade_core(self):
        raise NotImplementedError

    def trade(self):
        self._trade_core()

    def buy(self):
        pass # TODO: implement

    def sell(self):
        pass # TODO: implement
