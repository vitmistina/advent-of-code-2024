import unittest

from .aoc_2024_16 import main


class Test202416(unittest.TestCase):
    def test_day_2024_16(self):
        result = main("./2024_16/2024_16_test.txt")
        self.assertEqual(result["part_1"], 7036)
        result = main("./2024_16/2024_16_test_2.txt")
        self.assertEqual(result["part_1"], 11048)


if __name__ == "__main__":
    unittest.main()
