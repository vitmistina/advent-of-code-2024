import unittest

from .aoc_2024_07 import main


class Test202407(unittest.TestCase):
    def test_day_2024_07(self):
        result = main("./2024_07/2024_07_test.txt")
        self.assertEqual(result["part_1"], 3749)
        self.assertEqual(result["part_2"], 11387)


if __name__ == "__main__":
    unittest.main()
