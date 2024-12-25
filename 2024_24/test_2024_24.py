import unittest

from .aoc_2024_24 import main


class Test202424(unittest.TestCase):
    def test_day_2024_24(self):
        result = main("./2024_24/2024_24_test.txt")
        self.assertEqual(result["part_1"], 2024)


if __name__ == "__main__":
    unittest.main()
