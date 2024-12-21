import unittest

from .aoc_2024_20 import main


class Test202420(unittest.TestCase):
    def test_day_2024_20(self):
        result = main("./2024_20/2024_20_test.txt", 20)
        self.assertEqual(result["part_1"], 5)
        self.assertEqual(result["part_2"], 100)


if __name__ == "__main__":
    unittest.main()
