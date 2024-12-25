import unittest

from .aoc_2024_25 import main


class Test202425(unittest.TestCase):
    def test_day_2024_25(self):
        result = main("./2024_25/2024_25_test.txt")
        self.assertEqual(result["part_1"], 3)


if __name__ == "__main__":
    unittest.main()
