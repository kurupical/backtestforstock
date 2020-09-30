import unittest
from backtestforstock.trader import validate_date_step_interval
from datetime import timedelta

class TestValidateDateStepInterval(unittest.TestCase):
    def test_1m(self):
        expect = timedelta(minutes=1)
        actual = validate_date_step_interval("1m")
        self.assertEqual(expect, actual)

    def test_1h(self):
        expect = timedelta(hours=1)
        actual = validate_date_step_interval("1h")
        self.assertEqual(expect, actual)

    def test_1d(self):
        expect = timedelta(days=1)
        actual = validate_date_step_interval("1d")
        self.assertEqual(expect, actual)

    def test_error_format(self):
        with self.assertRaises(ValueError):
            validate_date_step_interval("10y")

    def test_error_format2(self):
        with self.assertRaises(ValueError):
            validate_date_step_interval("1yy")


class TestTrader(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()