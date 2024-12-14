import unittest

from .aoc_2024_14 import main


class Test202414(unittest.TestCase):
    def test_day_2024_14(self):
        result = main("./2024_14/2024_14_test.txt", 11, 7)
        self.assertEqual(result["part_1"], 12)
        self.assertEqual(result["part_2"], 100)


if __name__ == "__main__":
    unittest.main()
