import unittest

from .aoc_2024_10 import main


class Test202410(unittest.TestCase):
    def test_day_2024_10(self):
        result = main("./2024_10/2024_10_test.txt")
        self.assertEqual(result["part_1"], 36)
        self.assertEqual(result["part_2"], 81)


if __name__ == "__main__":
    unittest.main()
