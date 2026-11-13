import unittest

from pricing import total


class TotalTest(unittest.TestCase):
    def test_sums_lines(self):
        self.assertEqual(total([(2.50, 2), (1.25, 4)]), 10.00)
