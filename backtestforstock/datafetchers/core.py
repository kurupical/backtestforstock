

class DataFetcher:
    def __init__(self):
        pass

    def _fetch_core(self):
        raise NotImplementedError

    def fetch(self):
        self._fetch_core()