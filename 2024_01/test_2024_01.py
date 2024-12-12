import unittest

from .aoc_2024_01 import main


class Test202401(unittest.TestCase):
    def test_day_2024_01(self):
        result = main("./2024_01/2024_01_test.txt")
        self.assertEqual(result["part_1"], 11)
        self.assertEqual(result["part_2"], 31)


if __name__ == "__main__":
    unittest.main()
