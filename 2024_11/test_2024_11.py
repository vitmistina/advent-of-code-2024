import unittest

from aoc_2024_11 import main


class Test202411(unittest.TestCase):
    def test_day_2024_11(self):
        result = main("./2024_11/2024_11_test.txt")
        self.assertEqual(result["part_1"], 55312)


if __name__ == "__main__":
    unittest.main()
