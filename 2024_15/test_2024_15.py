import unittest

from .aoc_2024_15 import main


class Test202415(unittest.TestCase):
    def test_day_2024_15(self):
        small_result = main("./2024_15/2024_15_small_test.txt")
        self.assertEqual(small_result["part_1"], 2028)
        result = main("./2024_15/2024_15_test.txt")
        self.assertEqual(result["part_1"], 10092)
        self.assertEqual(result["part_2"], 9021)


if __name__ == "__main__":
    unittest.main()
