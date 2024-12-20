import unittest

from .aoc_2024_19 import main


class Test202419(unittest.TestCase):
    def test_day_2024_19(self):
        result = main("./2024_19/2024_19_test.txt")
        self.assertEqual(result["part_1"], 6)
        self.assertEqual(result["part_2"], 16)


if __name__ == "__main__":
    unittest.main()
