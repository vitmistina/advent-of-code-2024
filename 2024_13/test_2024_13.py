import unittest

from .aoc_2024_13 import main


class Test202413(unittest.TestCase):
    def test_day_2024_13(self):
        result = main("./2024_13/2024_13_test.txt")
        self.assertEqual(result["part_1"], 480)
        self.assertGreater(result["part_2"], 480)


if __name__ == "__main__":
    unittest.main()
