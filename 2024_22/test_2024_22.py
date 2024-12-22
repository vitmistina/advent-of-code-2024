import unittest

from .aoc_2024_22 import generate_nth_value, main


class Test202422(unittest.TestCase):
    def test_day_2024_22(self):
        result = main("./2024_22/2024_22_test.txt")
        self.assertEqual(result["part_1"], 37327623)
        result = main("./2024_22/2024_22_test_2.txt")
        self.assertEqual(result["part_2"], 23)

    def test_day_2024_22_generate(self):
        self.assertEqual(generate_nth_value(123, 10, {}), 5908254)


if __name__ == "__main__":
    unittest.main()
