import unittest

from .aoc_2024_09 import main


class Test202409(unittest.TestCase):
    def test_day_2024_09(self):
        result = main("./2024_09/2024_09_test.txt")
        self.assertEqual(result["part_1"], 1928)
        self.assertEqual(result["part_2"], 2858)


if __name__ == "__main__":
    unittest.main()
