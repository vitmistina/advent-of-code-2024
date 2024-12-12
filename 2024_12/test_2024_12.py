import unittest

from .aoc_2024_12 import main


class Test202412(unittest.TestCase):
    def test_day_2024_12(self):
        result = main("./2024_12/2024_12_test.txt")
        self.assertEqual(result["part_1"], 1930)
        self.assertEqual(result["part_2"], 1206)


if __name__ == "__main__":
    unittest.main()
