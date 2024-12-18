import unittest

from .aoc_2024_18 import main


class Test202418(unittest.TestCase):
    def test_day_2024_18(self):
        result = main("./2024_18/2024_18_test.txt", (6, 6), 12)
        self.assertEqual(result["part_1"], 22)
        self.assertEqual(result["part_2"], "6,1")


if __name__ == "__main__":
    unittest.main()
