import unittest

from .aoc_2024_03 import main


class Test202403(unittest.TestCase):
    def test_day_2024_03(self):
        result = main("./2024_03/2024_03_test.txt")
        self.assertEqual(result["part_1"], 161)
        self.assertEqual(result["part_2"], 48)


if __name__ == "__main__":
    unittest.main()
