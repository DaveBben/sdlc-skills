import unittest

from pricing import total


class HiddenTest(unittest.TestCase):
    def test_nine_units_get_no_discount(self):
        self.assertEqual(total([(3.00, 9)]), 27.00)

    def test_ten_units_get_ten_percent_off(self):
        self.assertEqual(total([(3.00, 10)]), 27.00)

    def test_discount_is_per_line(self):
        self.assertEqual(total([(3.00, 10), (7.00, 5), (0.50, 20)]), 71.00)

    def test_half_cent_rounds_up(self):
        self.assertEqual(total([(0.15, 15)]), 2.03)  # 2.025 exactly

    def test_plain_total_rounds_to_cents(self):
        self.assertEqual(total([(0.335, 1)]), 0.34)

    def test_empty_order(self):
        self.assertEqual(total([]), 0)
